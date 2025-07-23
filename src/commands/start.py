"""
Start Command - Welcome new users
"""

from core import keyboard, is_force_join_enabled, get_force_channels

def help():
    """Command help information"""
    return {
        "name": "start",
        "description": "Start the bot and show welcome message",
        "usage": "/start",
        "aliases": ["start", "begin"],
        "category": "basic",
        "examples": [
            "/start"
        ],
        "permissions": ["all"],
        "enabled": True
    }

async def start_command(bot, event):
    """Start command - welcome new users"""
    user_name = event.user.first_name if event.user else "User"

    # Get bot name from config
    bot_name = "Grandpa™ ORG"  # This should come from config

    text = f"""
🤖 <b>Welcome to {bot_name}, {user_name}!</b>

I'm your friendly assistant with clean, simple code!

<b>🚀 Commands:</b>
• /help - Show all commands
• /uid - Get your user ID
• /ping - Check bot response
    """

    # Add force join info if enabled
    if is_force_join_enabled():
        channels = get_force_channels()
        text += f"""

<b>📢 Official Channels:</b>
"""
        for channel_type, channel_username in channels.items():
            text += f"• {channel_username} - {channel_type.title()}\n"

    text += f"""

Thanks for using {bot_name}! 🚀
    """

    buttons = [
        [{"text": "🆔 Get ID", "callback_data": "get_uid"}],
        [{"text": "📋 Help", "callback_data": "help_menu"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, text.strip(), reply_markup=kb)

def register(handler):
    handler.add_command("start", start_command, help())
