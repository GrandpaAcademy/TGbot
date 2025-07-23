"""
Translator - Simple syntax wrapper for aiogram
Converts complex aiogram code to super simple, readable syntax
"""

import logging
import asyncio
from typing import Dict, Callable, Any, Optional
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .database import db
from .permissions import is_admin, is_banned, add_admin

logger = logging.getLogger(__name__)

class SimpleBot:
    """Simple bot wrapper that makes aiogram super easy to use"""
    
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()
        self.router = Router()
        self.dp.include_router(self.router)
        
        self.commands = {}
        self.events = {}
        
        logger.info("SimpleBot initialized")
    
    def command(self, name: str, description: str = "", admin_only: bool = False):
        """Decorator to register commands easily"""
        def decorator(func):
            # Store command info
            self.commands[name] = {
                'function': func,
                'description': description,
                'admin_only': admin_only
            }
            
            # Create aiogram handler
            async def handler(message: Message):
                # Add user to database
                user = message.from_user
                if user:
                    db.add_user(user.id, user.username, user.first_name, user.last_name)
                
                # Check if banned
                if user and is_banned(user.id):
                    await message.reply("❌ You are banned from using this bot.")
                    return
                
                # Check admin requirement
                if admin_only and not is_admin(user.id):
                    await message.reply("❌ This command is for admins only.")
                    return
                
                # Execute command
                try:
                    await func(self, message)
                except Exception as e:
                    logger.error(f"Error in command {name}: {e}")
                    await message.reply("❌ An error occurred.")
            
            # Register with aiogram
            self.router.message.register(handler, Command(commands=[name]))
            logger.info(f"Command '{name}' registered")
            
            return func
        return decorator
    
    def callback(self, data: str):
        """Decorator to register callback handlers"""
        def decorator(func):
            async def handler(callback: CallbackQuery):
                try:
                    await func(self, callback)
                    await callback.answer()
                except Exception as e:
                    logger.error(f"Error in callback {data}: {e}")
                    await callback.answer("❌ Error occurred")
            
            self.router.callback_query.register(handler, lambda c: c.data == data)
            logger.info(f"Callback '{data}' registered")
            
            return func
        return decorator
    
    def event(self, event_type: str):
        """Decorator to register event handlers"""
        def decorator(func):
            self.events[event_type] = func
            logger.info(f"Event '{event_type}' registered")
            return func
        return decorator
    
    async def send_message(self, chat_id: int, text: str, reply_markup=None):
        """Send message easily"""
        return await self.bot.send_message(chat_id, text, reply_markup=reply_markup)
    
    async def start_polling(self):
        """Start the bot"""
        logger.info("Starting bot polling...")
        await self.dp.start_polling(self.bot)

# Global bot instance
bot = None

def create_bot(token: str) -> SimpleBot:
    """Create a simple bot instance"""
    global bot
    bot = SimpleBot(token)
    return bot

def get_bot() -> Optional[SimpleBot]:
    """Get the current bot instance"""
    return bot

# Simple event class for compatibility
class Event:
    def __init__(self, message: Message):
        self.message = message
        self.chat = message.chat
        self.user = message.from_user
        self.text = message.text or ""

# Helper functions for the simple syntax
def keyboard(buttons):
    """Create inline keyboard from simple button data"""
    if not buttons:
        return None
    
    keyboard_buttons = []
    
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
            keyboard_buttons.append(button_row)
        else:
            if isinstance(row, dict):
                if 'url' in row:
                    keyboard_buttons.append([InlineKeyboardButton(text=row['text'], url=row['url'])])
                else:
                    keyboard_buttons.append([InlineKeyboardButton(text=row['text'], callback_data=row.get('callback_data', row['text']))])
            else:
                keyboard_buttons.append([InlineKeyboardButton(text=str(row), callback_data=str(row))])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

# Command handler class for the simple syntax
class CommandHandler:
    def __init__(self):
        self.commands = {}
    
    def add_command(self, name: str, func: Callable, help_info: Dict):
        """Add command with help info"""
        self.commands[name] = {
            'function': func,
            'help': help_info
        }
        
        # Register with the bot
        if bot:
            @bot.command(name, help_info.get('description', ''))
            async def wrapper(bot_instance, message):
                event = Event(message)
                await func(bot_instance, event)

# Global command handler
handler = CommandHandler()

# Compatibility functions
async def send_message(chat_id: int, text: str, reply_markup=None):
    """Send message using global bot"""
    if bot:
        return await bot.send_message(chat_id, text, reply_markup)

def register_command(name: str, func: Callable, help_info: Dict):
    """Register command with the global handler"""
    handler.add_command(name, func, help_info)

# Auto-load commands from modules
def load_command_module(module):
    """Load commands from a module with the simple syntax"""
    if hasattr(module, 'register'):
        module.register(handler)
    
    # Also check for individual command functions
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if callable(attr) and attr_name.endswith('_command'):
            command_name = attr_name.replace('_command', '')
            
            # Get help info if available
            help_info = {}
            if hasattr(module, 'help'):
                help_info = module.help()
            
            register_command(command_name, attr, help_info)
