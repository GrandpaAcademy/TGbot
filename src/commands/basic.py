from core import keyboard

def help():
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

# Start command
async def start_command(bot, event):
    """Start command - welcome new users"""
    user_name = event.user.first_name if event.user else "User"

    welcome_text = f"""
🤖 <b>Welcome to KOMI HUB 2, {user_name}!</b>

I'm your friendly assistant with clean, simple code!

<b>🚀 Quick Commands:</b>
• /start - This welcome message
• /help - Show all commands
• /uid - Get your user ID
• /ping - Check bot response
• /about - About this bot

<b>🎯 Features:</b>
• Super simple syntax
• Clean, readable code
• Easy to extend
• Modern aiogram backend

Thanks for using KOMI HUB 2! 🚀
    """

    buttons = [
        [{"text": "🆔 Get My ID", "callback_data": "get_uid"}],
        [{"text": "ℹ️ About Bot", "callback_data": "about_bot"}],
        [{"text": "📋 Help", "callback_data": "help_menu"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, welcome_text.strip(), reply_markup=kb)

# Help command
async def help_command(bot, event):
    """Help command - show available commands"""
    help_text = """
<b>🤖 KOMI HUB 2 - Command List</b>

<b>📋 Available Commands:</b>
• /start - Welcome message
• /help - This help message
• /uid - Get your user ID
• /ping - Check bot response
• /about - About this bot

<b>💡 How to use:</b>
• Type /command_name to execute any command
• Commands work in both private and group chats
• Some commands may require admin permissions

<i>Need more help? Contact support!</i>
    """

    buttons = [
        [{"text": "🏠 Back to Start", "callback_data": "back_start"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, help_text.strip(), reply_markup=kb)

# UID command
async def uid_command(bot, event):
    """UID command - get user information"""
    user = event.user
    chat = event.chat

    if user:
        uid_text = f"""
<b>🆔 Your Information:</b>

<b>User ID:</b> <code>{user.id}</code>
<b>Username:</b> @{user.username or 'None'}
<b>First Name:</b> {user.first_name or 'None'}
<b>Last Name:</b> {user.last_name or 'None'}
<b>Language:</b> {user.language_code or 'Unknown'}

<b>Chat ID:</b> <code>{chat.id}</code>
<b>Chat Type:</b> {chat.type}

<i>💡 Tip: You can copy IDs by tapping on them!</i>
        """
    else:
        uid_text = "❌ Unable to get user information."

    await bot.send_message(event.chat.id, uid_text.strip())

# Ping command
async def ping_command(bot, event):
    """Ping command - check bot response"""
    import time
    start_time = time.time()

    # Calculate response time
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)

    ping_text = f"""
🏓 <b>Pong!</b>

⚡ <b>Response Time:</b> <code>{response_time}ms</code>
🕐 <b>Current Time:</b> {time.strftime('%H:%M:%S')}

<i>Bot is running smoothly! 🚀</i>
    """

    await bot.send_message(event.chat.id, ping_text.strip())

# About command
async def about_command(bot, event):
    """About command - show bot information"""
    about_text = """
<b>🤖 About KOMI HUB 2</b>

<b>📊 Bot Information:</b>
• <b>Version:</b> 3.0.0
• <b>Framework:</b> aiogram 3.x (with simple syntax)
• <b>Language:</b> Python 3.12
• <b>Database:</b> SQLite

<b>🚀 Features:</b>
• Super simple command syntax
• Clean, readable code structure
• Easy to extend and modify
• Modern aiogram backend
• User management system

<b>👨‍💻 Developer:</b>
• <b>Team:</b> GrandpaAcademy
• <b>Architecture:</b> Simple & Clean
• <b>Code Style:</b> Readable & Maintainable

<i>Built with ❤️ using simple Python syntax!</i>
    """

    buttons = [
        [{"text": "🏠 Back to Start", "callback_data": "back_start"}],
        [{"text": "📋 Commands", "callback_data": "help_menu"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, about_text.strip(), reply_markup=kb)

def register(handler):
    """Register all basic commands"""
    handler.add_command("start", start_command, help())
    handler.add_command("help", help_command, {"description": "Show all available commands"})
    handler.add_command("uid", uid_command, {"description": "Get your user ID and information"})
    handler.add_command("ping", ping_command, {"description": "Check bot response time"})
    handler.add_command("about", about_command, {"description": "About this bot"})