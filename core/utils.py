"""
Utilities - Helper functions for the bot
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.warning(f"Config file {config_file} not found, creating default")
        default_config = {
            "token": "YOUR_BOT_TOKEN_HERE",
            "admins": [],
            "database": "bot.db",
            "log_level": "INFO"
        }
        save_config(default_config, config_file)
        return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

def save_config(config: Dict[str, Any], config_file: str = "config.json") -> bool:
    """Save configuration to JSON file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

def create_keyboard(buttons: list) -> InlineKeyboardMarkup:
    """Create inline keyboard from button data"""
    keyboard = []
    
    for row in buttons:
        if isinstance(row, list):
            button_row = []
            for btn in row:
                if isinstance(btn, dict):
                    if 'url' in btn:
                        button_row.append(InlineKeyboardButton(text=btn['text'], url=btn['url']))
                    else:
                        button_row.append(InlineKeyboardButton(text=btn['text'], callback_data=btn.get('callback_data', btn['text'])))
                else:
                    button_row.append(InlineKeyboardButton(text=str(btn), callback_data=str(btn)))
            keyboard.append(button_row)
        else:
            if isinstance(row, dict):
                if 'url' in row:
                    keyboard.append([InlineKeyboardButton(text=row['text'], url=row['url'])])
                else:
                    keyboard.append([InlineKeyboardButton(text=row['text'], callback_data=row.get('callback_data', row['text']))])
            else:
                keyboard.append([InlineKeyboardButton(text=str(row), callback_data=str(row))])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def format_time(seconds: int) -> str:
    """Format seconds into human readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_size(bytes_size: int) -> str:
    """Format bytes into human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def escape_markdown(text: str) -> str:
    """Escape Markdown special characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def get_user_mention(user) -> str:
    """Get user mention string"""
    if not user:
        return "Unknown User"
    
    name = user.first_name or "User"
    if user.username:
        return f"@{user.username}"
    else:
        return f"<a href='tg://user?id={user.id}'>{escape_html(name)}</a>"

def extract_args(text: str) -> list:
    """Extract arguments from command text"""
    parts = text.split()[1:]  # Remove command part
    return parts

def extract_user_id(text: str) -> Optional[int]:
    """Extract user ID from text"""
    try:
        # Try to extract from mention
        if text.startswith('@'):
            return None  # Username, not ID
        
        # Try to parse as number
        return int(text)
    except:
        return None

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self):
        self.user_timestamps: Dict[int, float] = {}
        self.rate_limit = 1  # 1 second default
    
    def is_rate_limited(self, user_id: int, limit_seconds: int = None) -> bool:
        """Check if user is rate limited"""
        if limit_seconds is None:
            limit_seconds = self.rate_limit
        
        current_time = time.time()
        
        if user_id in self.user_timestamps:
            time_diff = current_time - self.user_timestamps[user_id]
            if time_diff < limit_seconds:
                return True
        
        self.user_timestamps[user_id] = current_time
        return False
    
    def get_remaining_time(self, user_id: int, limit_seconds: int = None) -> float:
        """Get remaining time for rate limit"""
        if limit_seconds is None:
            limit_seconds = self.rate_limit
        
        if user_id not in self.user_timestamps:
            return 0
        
        current_time = time.time()
        time_diff = current_time - self.user_timestamps[user_id]
        remaining = limit_seconds - time_diff
        
        return max(0, remaining)

# Global rate limiter
rate_limiter = RateLimiter()

def get_uptime(start_time: datetime) -> str:
    """Get bot uptime"""
    uptime = datetime.now() - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
