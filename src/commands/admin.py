"""
Admin Commands - User management and bot control
"""

from core import is_admin, ban_user, unban_user, add_admin, db

def ban_help():
    """Ban command help information"""
    return {
        "name": "ban",
        "description": "Ban a user from using the bot",
        "usage": "/ban [reply to user] or /ban <user_id>",
        "aliases": ["ban", "block"],
        "category": "admin",
        "examples": [
            "/ban (reply to message)",
            "/ban 123456789"
        ],
        "permissions": ["admin"],
        "enabled": True
    }

def unban_help():
    """Unban command help information"""
    return {
        "name": "unban",
        "description": "Unban a user from the bot",
        "usage": "/unban [reply to user] or /unban <user_id>",
        "aliases": ["unban", "unblock"],
        "category": "admin",
        "examples": [
            "/unban (reply to message)",
            "/unban 123456789"
        ],
        "permissions": ["admin"],
        "enabled": True
    }

def addadmin_help():
    """Add admin command help information"""
    return {
        "name": "addadmin",
        "description": "Add a user as admin",
        "usage": "/addadmin [reply to user] or /addadmin <user_id>",
        "aliases": ["addadmin", "promote"],
        "category": "admin",
        "examples": [
            "/addadmin (reply to message)",
            "/addadmin 123456789"
        ],
        "permissions": ["admin"],
        "enabled": True
    }

def stats_help():
    """Stats command help information"""
    return {
        "name": "stats",
        "description": "Show bot statistics and user counts",
        "usage": "/stats",
        "aliases": ["stats", "statistics"],
        "category": "admin",
        "examples": [
            "/stats"
        ],
        "permissions": ["admin"],
        "enabled": True
    }

async def ban_command(bot, event):
    """Ban a user from using the bot"""
    if not is_admin(event.user.id):
        await bot.send_message(event.chat.id, "❌ Admin only.")
        return

    # Get target user ID
    target_id = None
    if hasattr(event.message, 'reply_to_message') and event.message.reply_to_message:
        target_id = event.message.reply_to_message.from_user.id
    else:
        args = event.text.split()[1:] if event.text else []
        if args:
            try:
                target_id = int(args[0])
            except ValueError:
                await bot.send_message(event.chat.id, "❌ Invalid user ID.")
                return

    if not target_id:
        await bot.send_message(event.chat.id, "❌ Reply to user or use /ban <user_id>")
        return

    if is_admin(target_id):
        await bot.send_message(event.chat.id, "❌ Cannot ban admin.")
        return

    if ban_user(target_id):
        await bot.send_message(event.chat.id, f"✅ User {target_id} banned.")
    else:
        await bot.send_message(event.chat.id, "❌ Failed to ban user.")

async def unban_command(bot, event):
    """Unban a user"""
    if not is_admin(event.user.id):
        await bot.send_message(event.chat.id, "❌ Admin only.")
        return

    # Get target user ID (same logic as ban)
    target_id = None
    if hasattr(event.message, 'reply_to_message') and event.message.reply_to_message:
        target_id = event.message.reply_to_message.from_user.id
    else:
        args = event.text.split()[1:] if event.text else []
        if args:
            try:
                target_id = int(args[0])
            except ValueError:
                await bot.send_message(event.chat.id, "❌ Invalid user ID.")
                return

    if not target_id:
        await bot.send_message(event.chat.id, "❌ Reply to user or use /unban <user_id>")
        return

    if unban_user(target_id):
        await bot.send_message(event.chat.id, f"✅ User {target_id} unbanned.")
    else:
        await bot.send_message(event.chat.id, "❌ Failed to unban user.")

async def addadmin_command(bot, event):
    """Add a user as admin"""
    if not is_admin(event.user.id):
        await bot.send_message(event.chat.id, "❌ Admin only.")
        return

    # Get target user ID
    target_id = None
    if hasattr(event.message, 'reply_to_message') and event.message.reply_to_message:
        target_id = event.message.reply_to_message.from_user.id
    else:
        args = event.text.split()[1:] if event.text else []
        if args:
            try:
                target_id = int(args[0])
            except ValueError:
                await bot.send_message(event.chat.id, "❌ Invalid user ID.")
                return

    if not target_id:
        await bot.send_message(event.chat.id, "❌ Reply to user or use /addadmin <user_id>")
        return

    if add_admin(target_id):
        await bot.send_message(event.chat.id, f"✅ User {target_id} is now admin.")
    else:
        await bot.send_message(event.chat.id, "❌ Failed to add admin.")

async def stats_command(bot, event):
    """Show bot statistics"""
    if not is_admin(event.user.id):
        await bot.send_message(event.chat.id, "❌ Admin only.")
        return

    total_users = db.get_user_count()
    all_users = db.get_all_users()

    admin_count = len([u for u in all_users if u['is_admin']])
    banned_count = len([u for u in all_users if u['is_banned']])

    text = f"""
<b>📊 Bot Statistics</b>

<b>Users:</b> {total_users}
<b>Active:</b> {total_users - banned_count}
<b>Banned:</b> {banned_count}
<b>Admins:</b> {admin_count}

<b>Status:</b> ✅ Online
<b>Version:</b> 3.0.0
    """

    await bot.send_message(event.chat.id, text.strip())

def register(handler):
    handler.add_command("ban", ban_command, ban_help())
    handler.add_command("unban", unban_command, unban_help())
    handler.add_command("addadmin", addadmin_command, addadmin_help())
    handler.add_command("stats", stats_command, stats_help())
