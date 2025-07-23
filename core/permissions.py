"""
Permissions System - Admin, ban, and pro user management
"""

import logging
from typing import Set
from .database import db

logger = logging.getLogger(__name__)

# In-memory admin cache for faster lookups
admin_cache: Set[int] = set()

def load_admins():
    """Load admins from database into cache"""
    try:
        users = db.get_all_users()
        admin_cache.clear()
        
        for user in users:
            if user['is_admin']:
                admin_cache.add(user['id'])
        
        logger.info(f"Loaded {len(admin_cache)} admins into cache")
        
    except Exception as e:
        logger.error(f"Error loading admins: {e}")

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    if not user_id:
        return False
    
    # Check cache first
    if user_id in admin_cache:
        return True
    
    # Check database
    user = db.get_user(user_id)
    if user and user['is_admin']:
        admin_cache.add(user_id)
        return True
    
    return False

def add_admin(user_id: int) -> bool:
    """Add user as admin"""
    try:
        db.set_admin(user_id, True)
        admin_cache.add(user_id)
        logger.info(f"User {user_id} added as admin")
        return True
        
    except Exception as e:
        logger.error(f"Error adding admin {user_id}: {e}")
        return False

def remove_admin(user_id: int) -> bool:
    """Remove user from admin"""
    try:
        db.set_admin(user_id, False)
        admin_cache.discard(user_id)
        logger.info(f"User {user_id} removed from admin")
        return True
        
    except Exception as e:
        logger.error(f"Error removing admin {user_id}: {e}")
        return False

def is_banned(user_id: int) -> bool:
    """Check if user is banned"""
    if not user_id:
        return False
    
    user = db.get_user(user_id)
    return user and user['is_banned']

def ban_user(user_id: int) -> bool:
    """Ban a user"""
    try:
        db.set_ban(user_id, True)
        logger.info(f"User {user_id} banned")
        return True
        
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return False

def unban_user(user_id: int) -> bool:
    """Unban a user"""
    try:
        db.set_ban(user_id, False)
        logger.info(f"User {user_id} unbanned")
        return True
        
    except Exception as e:
        logger.error(f"Error unbanning user {user_id}: {e}")
        return False

def is_pro(user_id: int) -> bool:
    """Check if user is pro"""
    if not user_id:
        return False
    
    user = db.get_user(user_id)
    return user and user['is_pro']

def set_pro(user_id: int, is_pro_user: bool = True) -> bool:
    """Set user pro status"""
    try:
        db.set_pro(user_id, is_pro_user)
        status = "added to" if is_pro_user else "removed from"
        logger.info(f"User {user_id} {status} pro")
        return True
        
    except Exception as e:
        logger.error(f"Error setting pro status for {user_id}: {e}")
        return False

def get_admin_list() -> list:
    """Get list of all admins"""
    try:
        users = db.get_all_users()
        admins = [user for user in users if user['is_admin']]
        return admins
        
    except Exception as e:
        logger.error(f"Error getting admin list: {e}")
        return []

def get_banned_list() -> list:
    """Get list of all banned users"""
    try:
        users = db.get_all_users()
        banned = [user for user in users if user['is_banned']]
        return banned
        
    except Exception as e:
        logger.error(f"Error getting banned list: {e}")
        return []

# Decorator for admin-only functions
def admin_required(func):
    """Decorator to require admin permissions"""
    async def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else None
        
        if not is_admin(user_id):
            await message.reply("❌ This command requires admin permissions.")
            return
        
        return await func(message, *args, **kwargs)
    
    return wrapper

# Decorator for ban check
def not_banned(func):
    """Decorator to check if user is not banned"""
    async def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else None
        
        if is_banned(user_id):
            await message.reply("❌ You are banned from using this bot.")
            return
        
        return await func(message, *args, **kwargs)
    
    return wrapper
