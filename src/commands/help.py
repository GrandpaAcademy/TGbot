"""
Help Command - Show available commands dynamically
"""

import os
import importlib.util
from core import keyboard, is_admin

def help():
    """Command help information"""
    return {
        "name": "help",
        "description": "Show all available commands and their usage",
        "usage": "/help [command_name]",
        "aliases": ["help", "commands", "cmd"],
        "category": "basic",
        "examples": [
            "/help",
            "/help start",
            "/help admin"
        ],
        "permissions": ["all"],
        "enabled": True
    }

def get_all_command_helps():
    """Dynamically get help info from all command files"""
    commands_dir = "src/commands"
    all_helps = {}

    if not os.path.exists(commands_dir):
        return all_helps

    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('_') and filename != 'help.py':
            module_name = filename[:-3]

            try:
                spec = importlib.util.spec_from_file_location(
                    f"commands.{module_name}",
                    os.path.join(commands_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Look for help functions in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and attr_name.endswith('_help') or attr_name == 'help':
                        try:
                            help_info = attr()
                            if isinstance(help_info, dict) and 'name' in help_info:
                                all_helps[help_info['name']] = help_info
                        except:
                            pass

            except Exception as e:
                pass

    return all_helps

async def help_command(bot, event):
    """Help command - show available commands dynamically"""
    user = event.user
    is_user_admin = is_admin(user.id if user else None)

    # Check if specific command help requested
    args = event.text.split()[1:] if event.text else []

    if args:
        command_name = args[0].lower()
        await show_specific_help(bot, event, command_name)
        return

    # Get all command helps dynamically
    all_helps = get_all_command_helps()

    # Group commands by category
    categories = {}
    for cmd_name, help_info in all_helps.items():
        category = help_info.get('category', 'other')
        permissions = help_info.get('permissions', ['all'])

        # Skip admin commands for non-admins
        if 'admin' in permissions and not is_user_admin:
            continue

        if category not in categories:
            categories[category] = []
        categories[category].append(help_info)

    # Build help text
    text = "<b>🤖 Grandpa™ ORG - Commands</b>\n\n"

    # Category icons
    category_icons = {
        'basic': '📋',
        'utility': '🔧',
        'fun': '🎮',
        'admin': '👑',
        'other': '📦'
    }

    for category, commands in categories.items():
        if not commands:
            continue

        icon = category_icons.get(category, '📦')
        text += f"<b>{icon} {category.title()}:</b>\n"

        for cmd_info in commands:
            name = cmd_info['name']
            desc = cmd_info['description']
            text += f"• /{name} - {desc}\n"

        text += "\n"

    text += "<i>💡 Use /help &lt;command&gt; for detailed info</i>"

    buttons = [
        [{"text": "🏠 Start", "callback_data": "back_start"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, text.strip(), reply_markup=kb)

async def show_specific_help(bot, event, command_name):
    """Show detailed help for specific command"""
    all_helps = get_all_command_helps()

    if command_name in all_helps:
        help_info = all_helps[command_name]

        text = f"<b>📖 Command Help: /{command_name}</b>\n\n"
        text += f"<b>📝 Description:</b>\n{help_info['description']}\n\n"
        text += f"<b>🔧 Usage:</b>\n<code>{help_info['usage']}</code>\n\n"

        if 'examples' in help_info and help_info['examples']:
            text += "<b>💡 Examples:</b>\n"
            for example in help_info['examples']:
                text += f"• <code>{example}</code>\n"
            text += "\n"

        if 'aliases' in help_info and help_info['aliases']:
            aliases = ', '.join([f"/{alias}" for alias in help_info['aliases']])
            text += f"<b>🔗 Aliases:</b> {aliases}\n\n"

        permissions = help_info.get('permissions', ['all'])
        if 'admin' in permissions:
            text += "<b>🔒 Permissions:</b> Admin only\n\n"

        text += f"<b>📂 Category:</b> {help_info.get('category', 'other').title()}"

    else:
        text = f"""
<b>❌ Command Not Found</b>

The command <code>/{command_name}</code> was not found.

Use /help to see all available commands.
        """

    buttons = [
        [{"text": "📋 All Commands", "callback_data": "help_menu"}],
        [{"text": "❌ Close", "callback_data": "close_menu"}]
    ]

    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, text.strip(), reply_markup=kb)

def register(handler):
    handler.add_command("help", help_command, help())
