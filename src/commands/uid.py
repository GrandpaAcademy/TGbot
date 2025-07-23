"""
UID Command - Get user and chat information
"""

from core import is_admin
import time

def help():
    """Command help information"""
    return {
        "name": "uid",
        "description": "Get user ID and detailed information",
        "usage": "/uid [reply to user] or /uid @username or /uid <user_id>",
        "aliases": ["uid", "id", "info", "me"],
        "category": "utility",
        "examples": [
            "/uid",
            "/uid @username",
            "/uid 123456789",
            "/uid (reply to message)"
        ],
        "permissions": ["all"],
        "enabled": True
    }

async def get_user_from_args(event):
    """Extract target user from command arguments or reply"""
    target_user = None
    target_user_id = None

    # Check if replying to a message
    if hasattr(event.message, 'reply_to_message') and event.message.reply_to_message:
        target_user = event.message.reply_to_message.from_user
        target_user_id = target_user.id if target_user else None
        return target_user, target_user_id

    # Check command arguments
    args = event.text.split()[1:] if event.text else []
    if not args:
        # No args, return current user
        return event.user, event.user.id if event.user else None

    arg = args[0]

    # Check if it's a username (@username)
    if arg.startswith('@'):
        try:
            # Try to get user info by username
            # Note: This requires bot to have seen the user before
            # In a real implementation, you'd use bot.get_chat(username)
            # For now, we'll return None and show error
            return None, None
        except:
            return None, None

    # Check if it's a user ID (numeric)
    elif arg.isdigit():
        user_id = int(arg)
        try:
            # Try to get user info by ID
            # Note: This requires bot to have interacted with user before
            # For now, we'll create a minimal user object
            return None, user_id
        except:
            return None, user_id

    return None, None

async def get_user_profile_info(bot, user_id):
    """Get detailed user profile information"""
    try:
        # Get user profile photos
        photos = await bot.bot.get_user_profile_photos(user_id, limit=1)
        has_photo = photos.total_count > 0

        # Try to get full user info
        try:
            chat_info = await bot.bot.get_chat(user_id)
            return {
                'has_photo': has_photo,
                'bio': getattr(chat_info, 'bio', None),
                'username': getattr(chat_info, 'username', None),
                'first_name': getattr(chat_info, 'first_name', None),
                'last_name': getattr(chat_info, 'last_name', None),
                'photos': photos if has_photo else None
            }
        except:
            return {
                'has_photo': has_photo,
                'bio': None,
                'username': None,
                'first_name': None,
                'last_name': None,
                'photos': photos if has_photo else None
            }
    except:
        return {
            'has_photo': False,
            'bio': None,
            'username': None,
            'first_name': None,
            'last_name': None,
            'photos': None
        }

async def get_chat_info(bot, chat):
    """Get detailed chat information"""
    chat_info = {
        'id': chat.id,
        'type': chat.type,
        'title': getattr(chat, 'title', None),
        'username': getattr(chat, 'username', None),
        'description': getattr(chat, 'description', None),
        'member_count': None,
        'admins_count': None
    }

    # Get additional info for groups/supergroups
    if chat.type in ['group', 'supergroup']:
        try:
            chat_full = await bot.bot.get_chat(chat.id)
            chat_info.update({
                'title': getattr(chat_full, 'title', chat_info['title']),
                'description': getattr(chat_full, 'description', None),
                'member_count': getattr(chat_full, 'member_count', None)
            })

            # Try to get admin count
            try:
                admins = await bot.bot.get_chat_administrators(chat.id)
                chat_info['admins_count'] = len(admins)
            except:
                pass
        except:
            pass

    return chat_info

async def uid_command(bot, event):
    """UID command - get user and chat information"""
    # Get target user
    target_user, target_user_id = await get_user_from_args(event)

    if not target_user_id:
        await bot.send_message(event.chat.id, "❌ Unable to get user information.")
        return

    # Get detailed user profile info
    profile_info = await get_user_profile_info(bot, target_user_id)

    # Use target_user info if available, otherwise use profile_info
    user_info = {
        'id': target_user_id,
        'username': target_user.username if target_user else profile_info['username'],
        'first_name': target_user.first_name if target_user else profile_info['first_name'],
        'last_name': target_user.last_name if target_user else profile_info['last_name'],
        'language_code': getattr(target_user, 'language_code', None) if target_user else None,
        'bio': profile_info['bio'],
        'has_photo': profile_info['has_photo'],
        'photos': profile_info['photos']
    }

    # Get chat information
    chat_info = await get_chat_info(bot, event.chat)

    # Build status
    status_parts = []
    if is_admin(target_user_id):
        status_parts.append("👑 Admin")
    else:
        status_parts.append("👤 User")

    # Check if user is admin in current chat (for groups)
    if chat_info['type'] in ['group', 'supergroup']:
        try:
            member = await bot.bot.get_chat_member(event.chat.id, target_user_id)
            if member.status in ['administrator', 'creator']:
                status_parts.append("🛡️ Chat Admin")
        except:
            pass

    status = " | ".join(status_parts)

    # Build user info text
    text = f"<b>🆔 User Information</b>\n\n"

    # Basic info
    text += f"<b>👤 Personal Details:</b>\n"
    text += f"• <b>User ID:</b> <code>{user_info['id']}</code>\n"
    text += f"• <b>Username:</b> @{user_info['username'] or 'None'}\n"
    text += f"• <b>First Name:</b> {user_info['first_name'] or 'None'}\n"

    if user_info['last_name']:
        text += f"• <b>Last Name:</b> {user_info['last_name']}\n"

    if user_info['language_code']:
        text += f"• <b>Language:</b> {user_info['language_code']}\n"

    text += f"• <b>Status:</b> {status}\n"

    # Bio if available
    if user_info['bio']:
        text += f"• <b>Bio:</b> {user_info['bio']}\n"

    # Profile photo status
    if user_info['has_photo']:
        text += f"• <b>Profile Photo:</b> ✅ Available\n"
    else:
        text += f"• <b>Profile Photo:</b> ❌ None\n"

    # Chat information
    text += f"\n<b>💬 Chat Details:</b>\n"
    text += f"• <b>Chat ID:</b> <code>{chat_info['id']}</code>\n"
    text += f"• <b>Chat Type:</b> {chat_info['type'].title()}\n"

    if chat_info['title']:
        text += f"• <b>Chat Title:</b> {chat_info['title']}\n"

    if chat_info['username']:
        text += f"• <b>Chat Username:</b> @{chat_info['username']}\n"

    if chat_info['description']:
        text += f"• <b>Description:</b> {chat_info['description'][:100]}{'...' if len(chat_info['description']) > 100 else ''}\n"

    if chat_info['member_count']:
        text += f"• <b>Members:</b> {chat_info['member_count']}\n"

    if chat_info['admins_count']:
        text += f"• <b>Admins:</b> {chat_info['admins_count']}\n"

    # Technical info
    text += f"\n<b>🔧 Technical Info:</b>\n"
    text += f"• <b>Message ID:</b> {event.message.message_id}\n"
    text += f"• <b>Date:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

    text += f"\n<i>💡 Tip: You can copy any ID by tapping on it!</i>"

    # Send profile photo if available
    if user_info['has_photo'] and user_info['photos']:
        try:
            photo = user_info['photos'].photos[0][-1]  # Get largest photo
            await bot.bot.send_photo(
                event.chat.id,
                photo.file_id,
                caption=text.strip(),
                parse_mode='HTML'
            )
        except:
            # Fallback to text message if photo fails
            await bot.send_message(event.chat.id, text.strip())
    else:
        await bot.send_message(event.chat.id, text.strip())

async def ping_command(bot, event):
    """Ping command - check bot response time"""
    start_time = time.time()
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)

    text = f"""
🏓 <b>Pong!</b>

⚡ Response: <code>{response_time}ms</code>
🕐 Time: {time.strftime('%H:%M:%S')}
✅ Status: Online

<i>Bot is running! 🚀</i>
    """

    await bot.send_message(event.chat.id, text.strip())

def ping_help():
    """Ping command help information"""
    return {
        "name": "ping",
        "description": "Check bot response time and status",
        "usage": "/ping",
        "aliases": ["ping", "pong"],
        "category": "utility",
        "examples": [
            "/ping"
        ],
        "permissions": ["all"],
        "enabled": True
    }

def register(handler):
    handler.add_command("uid", uid_command, help())
    handler.add_command("ping", ping_command, ping_help())
