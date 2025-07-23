"""
Example Commands - Template for creating new commands
This file shows the simple syntax structure for KOMI HUB 2
"""

from core import keyboard, is_admin, is_banned
import random
import time

def help():
    """
    Command help information - REQUIRED function
    This provides metadata about your commands
    """
    return {
        "name": "example",
        "description": "Example commands showing simple syntax",
        "usage": "/example, /demo, /test",
        "aliases": ["example", "demo", "test", "sample"],
        "category": "example",
        "examples": [
            "/example",
            "/demo hello world",
            "/test"
        ],
        "permissions": ["all"],  # or ["admin"] for admin-only
        "enabled": True
    }

# ============================================================================
# BASIC COMMAND STRUCTURE
# ============================================================================

async def example_command(bot, event):
    """
    Basic command example
    
    Args:
        bot: The bot instance (use for sending messages)
        event: Event object containing message, user, chat info
    """
    
    # Get user information
    user = event.user
    chat = event.chat
    message_text = event.text
    
    # Basic response
    response = f"""
🎯 <b>Example Command Response</b>

<b>👤 User Info:</b>
• Name: {user.first_name if user else 'Unknown'}
• ID: <code>{user.id if user else 'N/A'}</code>

<b>💬 Chat Info:</b>
• Chat ID: <code>{chat.id}</code>
• Chat Type: {chat.type}

<b>📝 Message:</b>
• Text: {message_text or 'No text'}
• Command: /example

<i>This is how simple commands work!</i>
    """
    
    # Send response
    await bot.send_message(event.chat.id, response.strip())

# ============================================================================
# COMMAND WITH ARGUMENTS
# ============================================================================

async def demo_command(bot, event):
    """
    Command that handles arguments
    Usage: /demo <your message>
    """
    
    # Get command arguments
    args = event.text.split()[1:] if event.text else []
    
    if not args:
        help_text = """
❌ <b>Missing Arguments</b>

<b>Usage:</b> <code>/demo &lt;your message&gt;</code>

<b>Examples:</b>
• <code>/demo hello world</code>
• <code>/demo this is a test</code>

<i>Try again with some text!</i>
        """
        await bot.send_message(event.chat.id, help_text.strip())
        return
    
    # Process arguments
    user_message = " ".join(args)
    
    response = f"""
🎤 <b>Demo Command</b>

<b>You said:</b> "{user_message}"
<b>Word count:</b> {len(args)} words
<b>Character count:</b> {len(user_message)} characters

<i>Your message has been processed!</i>
    """
    
    await bot.send_message(event.chat.id, response.strip())

# ============================================================================
# COMMAND WITH KEYBOARD BUTTONS
# ============================================================================

async def test_command(bot, event):
    """
    Command with interactive keyboard buttons
    """
    
    response = """
🧪 <b>Test Command</b>

This command demonstrates interactive buttons.
Click any button below to see how callbacks work!

<i>Choose an option:</i>
    """
    
    # Create keyboard buttons
    buttons = [
        [{"text": "🎲 Random Number", "callback_data": "random_number"}],
        [{"text": "🕐 Current Time", "callback_data": "current_time"}],
        [
            {"text": "👍 Like", "callback_data": "like"},
            {"text": "👎 Dislike", "callback_data": "dislike"}
        ],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]
    
    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, response.strip(), reply_markup=kb)

# ============================================================================
# ADMIN-ONLY COMMAND EXAMPLE
# ============================================================================

async def admin_example_command(bot, event):
    """
    Example admin-only command
    """
    
    user = event.user
    
    # Check if user is admin (manual check)
    if not is_admin(user.id):
        await bot.send_message(event.chat.id, "❌ This command requires admin privileges.")
        return
    
    # Check if user is banned (optional check)
    if is_banned(user.id):
        await bot.send_message(event.chat.id, "❌ You are banned from using this bot.")
        return
    
    admin_response = f"""
👑 <b>Admin Command Example</b>

<b>Welcome, Admin {user.first_name}!</b>

This command is only available to administrators.
You can add admin-only functionality here.

<b>🔧 Admin Features:</b>
• User management
• Bot configuration
• Statistics access
• System controls

<i>Use your powers wisely!</i>
    """
    
    buttons = [
        [{"text": "📊 View Stats", "callback_data": "admin_stats"}],
        [{"text": "👥 Manage Users", "callback_data": "manage_users"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]
    
    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, admin_response.strip(), reply_markup=kb)

# ============================================================================
# FUN COMMAND WITH RANDOM RESPONSES
# ============================================================================

async def fun_command(bot, event):
    """
    Fun command with random responses
    """
    
    # Random responses
    responses = [
        "🎉 You're awesome!",
        "🌟 Having a great day?",
        "🚀 Ready for adventure?",
        "💫 You're a star!",
        "🎯 Bullseye! Great choice!",
        "🔥 You're on fire!",
        "⚡ Electrifying!",
        "🌈 Colorful personality!",
        "🎪 Life's a circus, enjoy the show!",
        "🎭 You're quite the character!"
    ]
    
    # Random emojis
    emojis = ["🎲", "🎪", "🎨", "🎵", "🎮", "🎯", "🎊", "🎈"]
    
    selected_response = random.choice(responses)
    selected_emoji = random.choice(emojis)
    
    fun_text = f"""
{selected_emoji} <b>Fun Command</b>

{selected_response}

<b>🎲 Random Number:</b> {random.randint(1, 100)}
<b>🎯 Lucky Color:</b> {random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange'])}

<i>Keep having fun! 🎉</i>
    """
    
    await bot.send_message(event.chat.id, fun_text.strip())

# ============================================================================
# REGISTER FUNCTION - REQUIRED
# ============================================================================

def register(handler):
    """
    Register all commands - REQUIRED function
    
    This function is called automatically by the bot to register your commands.
    Add all your commands here using handler.add_command()
    
    Args:
        handler: Command handler instance
    """
    
    # Register basic commands
    handler.add_command("example", example_command, help())
    handler.add_command("demo", demo_command, {"description": "Demo command with arguments"})
    handler.add_command("test", test_command, {"description": "Test command with buttons"})
    
    # Register admin command (note: admin check is done inside the function)
    handler.add_command("adminexample", admin_example_command, {"description": "Admin example (Admin only)"})
    
    # Register fun command
    handler.add_command("fun", fun_command, {"description": "Fun command with random responses"})

# ============================================================================
# CALLBACK HANDLERS (Optional)
# ============================================================================
# 
# If you need callback handlers for your buttons, you can add them here
# or create a separate file in src/events/
#
# Example callback handler structure:
#
# from core import get_bot
# 
# def register_callbacks():
#     bot = get_bot()
#     
#     @bot.callback("random_number")
#     async def random_number_callback(bot_instance, callback):
#         number = random.randint(1, 1000)
#         await callback.message.edit_text(f"🎲 Random number: {number}")
#
# ============================================================================

# ============================================================================
# COMMAND STRUCTURE SUMMARY
# ============================================================================
#
# 1. Import required modules from core
# 2. Create help() function with command metadata
# 3. Create async command functions with (bot, event) parameters
# 4. Use event.user, event.chat, event.text for information
# 5. Use bot.send_message() to send responses
# 6. Use keyboard() function for interactive buttons
# 7. Create register() function to register all commands
# 8. Add admin checks manually if needed
#
# That's it! Super simple and clean! 🚀
# ============================================================================
