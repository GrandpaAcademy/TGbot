#!/usr/bin/env python3
"""
🤖 KOMI HUB 2 - Modern Telegram Bot
Clean, organized code structure with aiogram 3.x
"""

import asyncio
import logging
import importlib.util
import os
import io
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Import core modules
from core import (
    load_config, db, load_admins,
    create_bot, load_command_module
)

# Bot start time for uptime tracking
bot_start_time = datetime.now()

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def show_banner():
    """Show beautiful startup banner"""
    print(f'''\033[36m
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║   ██████╗ ██████╗  █████╗ ███╗   ██╗██████╗ ██████╗  █████╗                 ║
    ║  ██╔════╝ ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗                ║
    ║  ██║  ███╗██████╔╝███████║██╔██╗ ██║██║  ██║██████╔╝███████║                ║
    ║  ██║   ██║██╔══██╗██╔══██║██║╚██╗██║██║  ██║██╔═══╝ ██╔══██║                ║
    ║  ╚██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝██║     ██║  ██║                ║
    ║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝     ╚═╝  ╚═╝                ║
    ║                                                                               ║
    ║   █████╗  ██████╗ █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗                ║
    ║  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝                ║
    ║  ███████║██║     ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝                 ║
    ║  ██╔══██║██║     ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝                  ║
    ║  ██║  ██║╚██████╗██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║                   ║
    ║  ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝                   ║
    ║                                                                               ║
    ║                          🎓 Advanced Telegram Bot Framework                   ║
    ║                                  Version 3.0.0                               ║
    ║                                  Powered by aiogram 3.x                      ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
\033[0m''')

def load_commands():
    """Load all command modules with simple syntax"""
    commands_dir = "src/commands"
    if not os.path.exists(commands_dir):
        logging.warning(f"Commands directory '{commands_dir}' not found")
        return 0

    loaded_count = 0
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = filename[:-3]

            try:
                spec = importlib.util.spec_from_file_location(
                    f"commands.{module_name}",
                    os.path.join(commands_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Load with simple syntax translator
                load_command_module(module)
                loaded_count += 1
                logging.info(f"Loaded commands from {filename}")

            except Exception as e:
                logging.error(f"Error loading commands from {filename}: {e}")

    logging.info(f"Loaded {loaded_count} command modules")
    return loaded_count

def load_events(dp):
    """Load all event modules"""
    events_dir = "src/events"
    if not os.path.exists(events_dir):
        logging.warning(f"Events directory '{events_dir}' not found")
        return 0

    loaded_count = 0
    for filename in os.listdir(events_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = filename[:-3]

            try:
                spec = importlib.util.spec_from_file_location(
                    f"events.{module_name}",
                    os.path.join(events_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, 'register_events'):
                    module.register_events(dp)
                    loaded_count += 1
                    logging.info(f"Loaded events from {filename}")

            except Exception as e:
                logging.error(f"Error loading events from {filename}: {e}")

    # Register member events manually
    try:
        from src.events.member_events import handle_new_member, handle_left_member
        from core import get_bot

        bot = get_bot()
        if bot:
            # Register new member handler
            @bot.dp.message()
            async def new_member_handler(message):
                if message.new_chat_members:
                    await handle_new_member(bot, message)

            # Register left member handler
            @bot.dp.message()
            async def left_member_handler(message):
                if message.left_chat_member:
                    await handle_left_member(bot, message)

            logging.info("Loaded member events handlers")
            loaded_count += 1
    except Exception as e:
        logging.error(f"Error loading member events: {e}")

    logging.info(f"Loaded {loaded_count} event modules")
    return loaded_count

async def get_bot_info(token):
    """Get bot information from Telegram API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/bot{token}/getMe") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('result', {}).get('first_name', 'Unknown Bot')
                return 'Unknown Bot'
    except Exception as e:
        logging.error(f"Error getting bot info: {e}")
        return 'Unknown Bot'

async def main():
    """Main function to start the bot"""
    try:
        # Show banner
        show_banner()

        # Load configuration
        config = load_config()
        token = config.get('token')

        # Setup logging
        log_level = config.get('log_level', 'INFO')
        setup_logging(log_level)

        if not token or token == "YOUR_BOT_TOKEN_HERE":
            print("\033[31m❌ Configuration error: No token found\033[0m")
            return

        if not token or len(token) < 40 or ':' not in token:
            print("\033[31m❌ Invalid token format\033[0m")
            return

        print("\033[32m🔍 Fetching bot information...\033[0m")
        bot_name = await get_bot_info(token)

        print(f"\033[36m🤖 Bot Name: \033[1m{bot_name}\033[0m")
        print(f"\033[36m🔑 Token: \033[1m{'*' * (len(token) - 8)}{token[-8:]}\033[0m")
        print(f"\033[36m⏰ Started at: \033[1m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print(f"\033[36m🇧🇩 Timezone: Asia/Dhaka (UTC+6)\033[0m")
        print("\033[36m" + "=" * 79 + "\033[0m")

        print("\033[32m🚀 Initializing core systems...\033[0m")

        # Initialize database
        db.init_database()

        # Load admins from config
        admins = config.get('admins', [])
        for admin_id in admins:
            from core.permissions import add_admin
            add_admin(admin_id)

        load_admins()

        print("\033[32m🤖 Creating bot instance...\033[0m")

        # Create simple bot using translator
        bot = create_bot(token)

        print("\033[32m📁 Loading modules...\033[0m")

        # Load commands with simple syntax
        commands_loaded = load_commands()
        events_loaded = load_events(bot.dp)

        print(f"\033[32m✅ Loaded {commands_loaded} command modules and {events_loaded} event modules\033[0m")

        print("\033[32m🚀 KOMI HUB 2 Bot is starting...\033[0m")
        print("\033[32m📡 Starting polling for updates...\033[0m")

        # Start the bot
        await bot.start_polling()

    except KeyboardInterrupt:
        print("\033[33m\n👋 Bot stopped by user (Ctrl+C)\033[0m")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"\033[31m💥 Fatal error: {e}\033[0m")

if __name__ == "__main__":
    asyncio.run(main())
