"""
Command Handler - Clean, simple command management system
"""

import logging
import importlib
import importlib.util
import os
from typing import Dict, Callable, Any
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .database import db
from .permissions import is_admin, is_banned

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self):
        self.commands: Dict[str, Dict] = {}
        self.router = Router()
        
    def register_command(self, name: str, handler: Callable, description: str = "", 
                        admin_only: bool = False, group_only: bool = False):
        """Register a command"""
        self.commands[name] = {
            'handler': handler,
            'description': description,
            'admin_only': admin_only,
            'group_only': group_only
        }
        
        # Create wrapper function for aiogram
        async def command_wrapper(message: Message):
            await self.execute_command(name, message)
        
        # Register with aiogram router
        self.router.message.register(command_wrapper, Command(commands=[name]))
        logger.info(f"Command '{name}' registered successfully")
    
    async def execute_command(self, command_name: str, message: Message):
        """Execute a command with all checks"""
        try:
            if command_name not in self.commands:
                return
            
            command_info = self.commands[command_name]
            user = message.from_user
            
            # Add user to database
            if user:
                db.add_user(user.id, user.username, user.first_name, user.last_name)
            
            # Check if user is banned
            if user and is_banned(user.id):
                await message.reply("❌ You are banned from using this bot.")
                return
            
            # Check admin requirement
            if command_info['admin_only'] and not is_admin(user.id):
                await message.reply("❌ This command is for admins only.")
                return
            
            # Check group requirement
            if command_info['group_only'] and message.chat.type == 'private':
                await message.reply("❌ This command can only be used in groups.")
                return
            
            # Execute command
            await command_info['handler'](message)
            logger.info(f"Command '{command_name}' executed by user {user.id if user else 'unknown'}")
            
        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}")
            await message.reply("❌ An error occurred while executing the command.")
    
    def get_commands_list(self, user_id: int = None) -> str:
        """Get formatted list of available commands"""
        user_is_admin = is_admin(user_id) if user_id else False
        
        general_commands = []
        admin_commands = []
        
        for name, info in self.commands.items():
            if info['admin_only']:
                if user_is_admin:
                    admin_commands.append(f"/{name} - {info['description']}")
            else:
                general_commands.append(f"/{name} - {info['description']}")
        
        result = "<b>📋 Available Commands:</b>\n\n"
        
        if general_commands:
            result += "<b>🔹 General Commands:</b>\n"
            result += "\n".join(general_commands) + "\n\n"
        
        if admin_commands and user_is_admin:
            result += "<b>🔸 Admin Commands:</b>\n"
            result += "\n".join(admin_commands)
        
        return result
    
    def load_commands_from_directory(self, directory: str = "src/commands"):
        """Load all commands from directory"""
        if not os.path.exists(directory):
            logger.warning(f"Commands directory '{directory}' not found")
            return
        
        loaded_count = 0
        
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]  # Remove .py extension
                
                try:
                    # Import the module
                    spec = importlib.util.spec_from_file_location(
                        f"commands.{module_name}", 
                        os.path.join(directory, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Register commands from module
                    if hasattr(module, 'register_commands'):
                        module.register_commands(self)
                        loaded_count += 1
                        logger.info(f"Loaded commands from {filename}")
                    
                except Exception as e:
                    logger.error(f"Error loading commands from {filename}: {e}")
        
        logger.info(f"Loaded {loaded_count} command modules")

# Global command handler
command_handler = CommandHandler()

# Helper functions for easy command registration
def command(name: str, description: str = "", admin_only: bool = False, group_only: bool = False):
    """Decorator for registering commands"""
    def decorator(func):
        command_handler.register_command(name, func, description, admin_only, group_only)
        return func
    return decorator

def load_all_commands():
    """Load all commands from src/commands directory"""
    command_handler.load_commands_from_directory("src/commands")
