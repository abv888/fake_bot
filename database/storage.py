import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import logging

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    cursor_factory=RealDictCursor
                )
            return self.conn
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            return None
    
    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            conn = self.get_connection()
            if conn is None:
                return
                
            cursor = conn.cursor()
            
            # Create users table with traffic source tracking
            cursor.execute('''
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
            
            # Create index on user_id for faster lookups
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)
            ''')
            
            # Create index on traffic_source for analytics
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_traffic_source ON users(traffic_source)
            ''')
            
            conn.commit()
            logging.info("Database initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                 last_name: str = None, traffic_source: str = None) -> bool:
        """Add a new user to the database or update if exists"""
        try:
            conn = self.get_connection()
            if conn is None:
                return False
                
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update user data (but keep original traffic_source)
                cursor.execute(
                    "UPDATE users SET username = %s, first_name = %s, last_name = %s WHERE user_id = %s",
                    (username, first_name, last_name, user_id)
                )
                logging.info(f"Updated existing user: {user_id}")
            else:
                # Insert new user
                cursor.execute(
                    """INSERT INTO users (user_id, username, first_name, last_name, traffic_source) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user_id, username, first_name, last_name, traffic_source)
                )
                logging.info(f"Added new user: {user_id} from source: {traffic_source}")
            
            conn.commit()
            return True
            
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            return False
    
    def track_button_click(self, user_id: int) -> bool:
        """Track when user clicks the mini app button"""
        try:
            conn = self.get_connection()
            if conn is None:
                return False
                
            cursor = conn.cursor()
            
            cursor.execute(
                """UPDATE users SET button_clicked = TRUE, button_clicked_at = CURRENT_TIMESTAMP 
                   WHERE user_id = %s""",
                (user_id,)
            )
            
            conn.commit()
            logging.info(f"Tracked button click for user: {user_id}")
            return True
            
        except Exception as e:
            logging.error(f"Error tracking button click: {e}")
            return False
    
    def get_user_stats(self, traffic_source: str = None) -> Dict:
        """Get user statistics by traffic source"""
        try:
            conn = self.get_connection()
            if conn is None:
                return {}
                
            cursor = conn.cursor()
            
            if traffic_source:
                # Stats for specific traffic source
                cursor.execute(
                    """SELECT 
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                        COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) as click_rate
                       FROM users WHERE traffic_source = %s""",
                    (traffic_source,)
                )
            else:
                # Overall stats
                cursor.execute(
                    """SELECT 
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                        COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) as click_rate
                       FROM users"""
                )
            
            result = cursor.fetchone()
            return dict(result) if result else {}
            
        except Exception as e:
            logging.error(f"Error getting user stats: {e}")
            return {}
    
    def get_traffic_sources_stats(self) -> List[Dict]:
        """Get statistics for all traffic sources"""
        try:
            conn = self.get_connection()
            if conn is None:
                return []
                
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT 
                    traffic_source,
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) as clicked_users,
                    COUNT(CASE WHEN button_clicked = TRUE THEN 1 END) * 100.0 / COUNT(*) as click_rate
                   FROM users 
                   WHERE traffic_source IS NOT NULL
                   GROUP BY traffic_source
                   ORDER BY total_users DESC"""
            )
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logging.error(f"Error getting traffic sources stats: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logging.info("Database connection closed")