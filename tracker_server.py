import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import urllib.parse
import json
from datetime import datetime

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.storage import DatabaseManager

app = Flask(__name__)
CORS(app, origins="*")

# Инициализируем менеджер базы данных
db = DatabaseManager()

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
        parsed_data = urllib.parse.parse_qs(init_data)
        user_json = parsed_data.get('user', ['{}'])[0]
        user_data = json.loads(user_json) if user_json != '{}' else {}
        return user_data.get('id'), user_data
    except Exception as e:
        logger.error(f"Error parsing telegram data: {e}")
        return None, None

@app.route('/api/track-click', methods=['POST', 'OPTIONS'])
def track_click():
    """Эндпоинт для трекинга кликов"""
    
    # CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        init_data = data.get('init_data', '')
        click_type = data.get('click_type', 'website_click')
        
        # Парсим данные пользователя
        user_id, user_data = parse_telegram_data(init_data)
        
        if not user_id:
            logger.warning("No valid user_id found in request")
            return jsonify({'error': 'Invalid user data'}), 400
        
        # Трекаем клик в базе данных
        success = db.track_button_click(user_id)
        
        if success:
            logger.info(f"Successfully tracked {click_type} for user {user_id}")
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
            logger.error(f"Failed to track click for user {user_id}")
            return jsonify({'error': 'Failed to track click'}), 500
            
    except Exception as e:
        logger.error(f"Error in track_click endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервера"""
    try:
        # Проверяем подключение к базе данных
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
    return jsonify({
        'message': 'IOST Tracker is working!',
        'server_ip': '185.193.125.110',
        'timestamp': datetime.now().isoformat(),
        'method': request.method
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