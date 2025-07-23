"""
Database Handler - Simple SQLite database for user management
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_admin INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    is_pro INTEGER DEFAULT 0,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Chat settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_settings (
                    chat_id INTEGER PRIMARY KEY,
                    chat_title TEXT,
                    welcome_enabled INTEGER DEFAULT 1,
                    rules_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bot statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_stats (
                    id INTEGER PRIMARY KEY,
                    total_users INTEGER DEFAULT 0,
                    total_commands INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Add or update user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users (id, username, first_name, last_name, last_seen)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, datetime.now()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0], 'username': row[1], 'first_name': row[2], 'last_name': row[3],
                    'is_admin': bool(row[4]), 'is_banned': bool(row[5]), 'is_pro': bool(row[6]),
                    'join_date': row[7], 'last_seen': row[8]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def set_admin(self, user_id: int, is_admin: bool = True):
        """Set user admin status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_admin = ? WHERE id = ?', (int(is_admin), user_id))
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting admin status for {user_id}: {e}")
    
    def set_ban(self, user_id: int, is_banned: bool = True):
        """Set user ban status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_banned = ? WHERE id = ?', (int(is_banned), user_id))
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting ban status for {user_id}: {e}")
    
    def set_pro(self, user_id: int, is_pro: bool = True):
        """Set user pro status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_pro = ? WHERE id = ?', (int(is_pro), user_id))
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting pro status for {user_id}: {e}")
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            conn.close()
            
            users = []
            for row in rows:
                users.append({
                    'id': row[0], 'username': row[1], 'first_name': row[2], 'last_name': row[3],
                    'is_admin': bool(row[4]), 'is_banned': bool(row[5]), 'is_pro': bool(row[6]),
                    'join_date': row[7], 'last_seen': row[8]
                })
            
            return users
            
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def get_user_count(self) -> int:
        """Get total user count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0

# Global database instance
db = Database()
