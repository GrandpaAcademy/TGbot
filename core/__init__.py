"""
Core Module - Clean, simple bot framework
"""

from .database import db, Database
from .command_handler import command_handler, command, load_all_commands
from .permissions import (
    is_admin, add_admin, remove_admin,
    is_banned, ban_user, unban_user,
    is_pro, set_pro,
    admin_required, not_banned,
    load_admins
)
from .hot_reload import hot_reloader, reload_commands, reload_events, reload_all, auto_reload
from .utils import (
    load_config, save_config, create_keyboard,
    format_time, format_size, escape_html, escape_markdown,
    get_user_mention, extract_args, extract_user_id,
    rate_limiter, get_uptime
)
from .translator import (
    SimpleBot, create_bot, get_bot, Event,
    keyboard, CommandHandler, handler,
    send_message, register_command, load_command_module
)
from .force_join import (
    check_force_join, is_force_join_enabled, get_force_channels, force_join
)

__all__ = [
    # Database
    'db', 'Database',

    # Command handling
    'command_handler', 'command', 'load_all_commands',

    # Permissions
    'is_admin', 'add_admin', 'remove_admin',
    'is_banned', 'ban_user', 'unban_user',
    'is_pro', 'set_pro',
    'admin_required', 'not_banned',
    'load_admins',

    # Hot reload
    'hot_reloader', 'reload_commands', 'reload_events', 'reload_all', 'auto_reload',

    # Utils
    'load_config', 'save_config', 'create_keyboard',
    'format_time', 'format_size', 'escape_html', 'escape_markdown',
    'get_user_mention', 'extract_args', 'extract_user_id',
    'rate_limiter', 'get_uptime',

    # Simple Translator
    'SimpleBot', 'create_bot', 'get_bot', 'Event',
    'keyboard', 'CommandHandler', 'handler',
    'send_message', 'register_command', 'load_command_module',

    # Force Join
    'check_force_join', 'is_force_join_enabled', 'get_force_channels', 'force_join'
]
