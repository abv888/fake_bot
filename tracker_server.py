#!/usr/bin/env python3

import os
import sys
from flask import Flask, request, jsonify
import logging
import urllib.parse
import json
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ВАЖНО: Используем старый синхронный DatabaseManager для Flask
from database.storage import AsyncDatabaseManager

app = Flask(__name__)

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    return response

# Используем синхронный менеджер базы данных
db = AsyncDatabaseManager()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tracker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def parse_telegram_data(init_data):
    """Парсинг данных от Telegram WebApp"""
    try:
        logger.info(f"Parsing init_data: {init_data[:100]}...")
        
        parsed_data = urllib.parse.parse_qs(init_data)
        user_json = parsed_data.get('user', ['{}'])[0]
        
        logger.info(f"User JSON: {user_json}")
        
        user_data = json.loads(user_json) if user_json != '{}' else {}
        user_id = user_data.get('id')
        
        logger.info(f"Extracted user_id: {user_id}")
        
        return user_id, user_data
    except Exception as e:
        logger.error(f"Error parsing telegram data: {e}")
        return None, None

@app.route('/api/track-click', methods=['POST', 'OPTIONS'])
def track_click():
    """Эндпоинт для трекинга кликов"""
    
    # CORS preflight
    if request.method == 'OPTIONS':
        logger.info("CORS preflight request received")
        return jsonify({'status': 'ok'})
    
    logger.info("=== TRACK CLICK REQUEST ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Remote addr: {request.remote_addr}")
    
    try:
        # Получаем данные запроса
        raw_data = request.get_data(as_text=True)
        logger.info(f"Raw request data: {raw_data}")
        
        data = request.get_json()
        logger.info(f"Parsed JSON data: {data}")
        
        if not data:
            logger.error("No data provided in request")
            return jsonify({'error': 'No data provided'}), 400
        
        init_data = data.get('init_data', '')
        click_type = data.get('click_type', 'website_click')
        
        logger.info(f"Click type: {click_type}")
        logger.info(f"Init data present: {bool(init_data)}")
        
        # Парсим данные пользователя
        user_id, user_data = parse_telegram_data(init_data)
        
        if not user_id:
            logger.warning("No valid user_id found in request")
            return jsonify({'error': 'Invalid user data'}), 400
        
        logger.info(f"Processing click for user_id: {user_id}")
        
        # ИСПРАВЛЕНО: используем синхронный метод
        success = db.track_button_click(user_id)
        
        if success:
            logger.info(f"✅ Successfully tracked {click_type} for user {user_id}")
            response_data = {
                'success': True,
                'message': 'Click tracked successfully',
                'user_id': user_id,
                'click_type': click_type,
                'timestamp': datetime.now().isoformat()
            }
            
            if user_data:
                response_data['user_name'] = user_data.get('first_name', 'Unknown')
            
            return jsonify(response_data)
        else:
            logger.error(f"❌ Failed to track click for user {user_id}")
            return jsonify({'error': 'Failed to track click in database'}), 500
            
    except Exception as e:
        logger.error(f"🚨 Error in track_click endpoint: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервера"""
    try:
        # ИСПРАВЛЕНО: используем синхронный метод
        stats = db.get_user_stats()
        
        return jsonify({
            'status': 'ok',
            'service': 'IOST Click Tracker',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'total_users': stats.get('total_users', 0) if stats else 0
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'service': 'IOST Click Tracker',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Получить статистику (для админов)"""
    try:
        # ИСПРАВЛЕНО: используем синхронные методы
        overall_stats = db.get_user_stats()
        traffic_stats = db.get_traffic_sources_stats()
        
        return jsonify({
            'overall': overall_stats,
            'traffic_sources': traffic_stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Тестовый эндпоинт"""
    logger.info(f"Test endpoint called with method: {request.method}")
    return jsonify({
        'message': 'IOST Tracker is working!',
        'server_ip': '185.193.125.110',
        'timestamp': datetime.now().isoformat(),
        'method': request.method
    })

@app.route('/api/debug', methods=['POST'])
def debug_endpoint():
    """Отладочный эндпоинт для проверки запросов"""
    logger.info("=== DEBUG ENDPOINT ===")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Data: {request.get_data(as_text=True)}")
    logger.info(f"JSON: {request.get_json()}")
    
    return jsonify({
        'received_headers': dict(request.headers),
        'received_data': request.get_data(as_text=True),
        'received_json': request.get_json(),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Создаем папку для логов если её нет
    os.makedirs('logs', exist_ok=True)
    
    logger.info("Starting IOST Click Tracker Server...")
    
    # Получаем порт из переменных окружения или используем 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Запускаем сервер
    app.run(
        host='0.0.0.0',  # Слушаем на всех интерфейсах
        port=port,
        debug=False,
        threaded=True
    )