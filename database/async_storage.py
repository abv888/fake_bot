import asyncpg
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

class AsyncDatabaseManager:
    def __init__(self):
        self.pool = None
        self.logger = logging.getLogger(__name__)
        self._initialized = False  # Флаг инициализации
    
    async def init_pool(self):
        """Инициализация пула соединений"""
        if self._initialized:
            return  # Уже инициализирован
            
        try:
            self.pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                min_size=1,
                max_size=10,
                command_timeout=60,
                server_settings={
                    'jit': 'off'  # Отключает JIT для стабильности
                }
            )
            self.logger.info("Async database pool initialized successfully")
            await self.init_tables()
            self._initialized = True
        except Exception as e:
            self.logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close_pool(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
            self.logger.info("Database pool closed")
            self._initialized = False
    
    @asynccontextmanager
    async def get_connection(self):
        """Контекстный менеджер для получения соединения из пула"""
        if not self.pool or not self._initialized:
            await self.init_pool()
        
        try:
            async with self.pool.acquire() as connection:
                yield connection
        except Exception as e:
            self.logger.error(f"Error acquiring database connection: {e}")
            raise
    
    async def init_tables(self):
        """Создание таблиц в базе данных"""
        try:
            async with self.get_connection() as conn:
                # Создание таблицы пользователей
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT UNIQUE NOT NULL,
                        username VARCHAR(255),
                        first_name VARCHAR(255),
                        last_name VARCHAR(255),
                        traffic_source VARCHAR(255),
                        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        button_clicked BOOLEAN DEFAULT FALSE,
                        button_clicked_at TIMESTAMP
                    )
                ''')
                
                # Создание индексов
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_traffic_source ON users(traffic_source)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_registered_at ON users(registered_at)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_button_clicked ON users(button_clicked)')
                
                self.logger.info("Database tables initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing tables: {e}")
            raise
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                      last_name: str = None, traffic_source: str = None) -> bool:
        """Добавление или обновление пользователя"""
        try:
            async with self.get_connection() as conn:
                # Используем UPSERT (INSERT ... ON CONFLICT) для атомарности
                await conn.execute(
                    """INSERT INTO users (user_id, username, first_name, last_name, traffic_source) 
                       VALUES ($1, $2, $3, $4, $5)
                       ON CONFLICT (user_id) 
                       DO UPDATE SET 
                           username = EXCLUDED.username,
                           first_name = EXCLUDED.first_name,
                           last_name = EXCLUDED.last_name""",
                    user_id, username, first_name, last_name, traffic_source
                )
                
                self.logger.info(f"Added/updated user: {user_id} from source: {traffic_source}")
                return True
        except Exception as e:
            self.logger.error(f"Error adding user {user_id}: {e}")
            return False
    
    async def track_button_click(self, user_id: int) -> bool:
        """Отслеживание клика по кнопке"""
        try:
            async with self.get_connection() as conn:
                result = await conn.execute(
                    """UPDATE users SET button_clicked = TRUE, button_clicked_at = CURRENT_TIMESTAMP 
                       WHERE user_id = $1""",
                    user_id
                )
                
                # Проверяем, была ли обновлена строка
                if result == "UPDATE 1":
                    self.logger.info(f"Tracked button click for user: {user_id}")
                    return True
                else:
                    self.logger.warning(f"User {user_id} not found for button click tracking")
                    return False
        except Exception as e:
            self.logger.error(f"Error tracking button click for user {user_id}: {e}")
            return False
    
    async def get_user_stats(self, traffic_source: str = None) -> Dict:
        """Получение статистики пользователей"""
        try:
            async with self.get_connection() as conn:
                if traffic_source:
                    # Статистика для конкретного источника трафика
                    row = await conn.fetchrow(
                        """SELECT 
                            COUNT(*) as total_users,
                            COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                            ROUND(
                                CASE 
                                    WHEN COUNT(*) = 0 THEN 0 
                                    ELSE COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) 
                                END, 2
                            ) as click_rate
                           FROM users WHERE traffic_source = $1""",
                        traffic_source
                    )
                else:
                    # Общая статистика
                    row = await conn.fetchrow(
                        """SELECT 
                            COUNT(*) as total_users,
                            COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                            ROUND(
                                CASE 
                                    WHEN COUNT(*) = 0 THEN 0 
                                    ELSE COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) 
                                END, 2
                            ) as click_rate
                           FROM users"""
                    )
                
                return dict(row) if row else {}
        except Exception as e:
            self.logger.error(f"Error getting user stats: {e}")
            return {}
    
    async def get_traffic_sources_stats(self) -> List[Dict]:
        """Получение статистики по источникам трафика"""
        try:
            async with self.get_connection() as conn:
                rows = await conn.fetch(
                    """SELECT 
                        traffic_source,
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                        ROUND(
                            CASE 
                                WHEN COUNT(*) = 0 THEN 0 
                                ELSE COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) 
                            END, 2
                        ) as click_rate
                       FROM users 
                       WHERE traffic_source IS NOT NULL
                       GROUP BY traffic_source
                       ORDER BY total_users DESC"""
                )
                
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting traffic sources stats: {e}")
            return []
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Получение пользователя по ID"""
        try:
            async with self.get_connection() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM users WHERE user_id = $1", user_id
                )
                return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Получение списка всех пользователей"""
        try:
            async with self.get_connection() as conn:
                rows = await conn.fetch(
                    """SELECT user_id, username, first_name, traffic_source, 
                              registered_at, button_clicked, button_clicked_at
                       FROM users 
                       ORDER BY registered_at DESC 
                       LIMIT $1 OFFSET $2""",
                    limit, offset
                )
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting all users: {e}")
            return []
    
    async def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        try:
            async with self.get_connection() as conn:
                result = await conn.execute(
                    "DELETE FROM users WHERE user_id = $1", user_id
                )
                
                if result == "DELETE 1":
                    self.logger.info(f"Deleted user: {user_id}")
                    return True
                else:
                    self.logger.warning(f"User {user_id} not found for deletion")
                    return False
        except Exception as e:
            self.logger.error(f"Error deleting user {user_id}: {e}")
            return False
    
    async def health_check(self) -> bool:
        """Проверка состояния базы данных"""
        try:
            async with self.get_connection() as conn:
                await conn.fetchval("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False

# Глобальный экземпляр для использования в боте
async_db = AsyncDatabaseManager()