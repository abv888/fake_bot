import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

class DatabaseManager:
    def __init__(self, db_path: str = "casino_guide_bot.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registered_at TIMESTAMP,
            conference_registered BOOLEAN DEFAULT 0
        )
        ''')
        
        # Create webinar registration table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conference_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            registered_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
        """Add a new user to the database or update if exists"""
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now()
            
            # Check if user exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update user data
                cursor.execute(
                    "UPDATE users SET username = ?, first_name = ?, last_name = ? WHERE user_id = ?",
                    (username, first_name, last_name, user_id)
                )
            else:
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (user_id, username, first_name, last_name, registered_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username, first_name, last_name, current_time)
                )
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def register_for_conference(self, user_id: int) -> bool:
        """Register user for the webinar"""
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now()
            
            # Update user's webinar registration status
            cursor.execute(
                "UPDATE users SET conference_registered = 1 WHERE user_id = ?",
                (user_id,)
            )
            
            # Add registration record
            cursor.execute(
                "INSERT INTO conference_registrations (user_id, registered_at) VALUES (?, ?)",
                (user_id, current_time)
            )
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error registering for webinar: {e}")
            return False
    
    def is_registered_for_conference(self, user_id: int) -> bool:
        """Check if user is registered for webinar"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT conference_registered FROM users WHERE user_id = ?",
                (user_id,)
            )
            
            result = cursor.fetchone()
            if result and result[0] == 1:
                return True
            return False
        except Exception as e:
            print(f"Error checking webinar registration: {e}")
            return False
    
    def get_all_conference_users(self) -> List[int]:
        """Get all users registered for the webinar"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT user_id FROM users WHERE conference_registered = 1"
            )
            
            result = cursor.fetchall()
            return [row[0] for row in result]
        except Exception as e:
            print(f"Error getting webinar users: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()