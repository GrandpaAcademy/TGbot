from core import get_bot, keyboard
from core.force_join import force_join

def register_events(dp):
    """Register callback events with simple syntax"""
    bot = get_bot()
    
    if not bot:
        return
    
    @bot.callback("get_uid")
    async def get_uid_callback(bot_instance, callback):
        """Get user ID callback"""
        user = callback.from_user
        
        uid_text = f"""
<b>🆔 Your Information:</b>

<b>User ID:</b> <code>{user.id}</code>
<b>Username:</b> @{user.username or 'None'}
<b>First Name:</b> {user.first_name or 'None'}
<b>Language:</b> {user.language_code or 'Unknown'}

<i>💡 Tip: You can copy your ID by tapping on it!</i>
        """
        
        buttons = [
            [{"text": "🏠 Back to Start", "callback_data": "back_start"}],
            [{"text": "❌ Close", "callback_data": "close_menu"}]
        ]
        
        kb = keyboard(buttons)
        await callback.message.edit_text(uid_text.strip(), reply_markup=kb)
    
    @bot.callback("about_bot")
    async def about_bot_callback(bot_instance, callback):
        """About bot callback"""
        about_text = """
<b>🤖 KOMI HUB 2</b>

<b>Version:</b> 3.0.0
<b>Framework:</b> aiogram 3.x (simple syntax)
<b>Language:</b> Python 3.12

<b>🚀 Features:</b>
• Super simple command syntax
• Clean, readable code
• Easy to extend
• Modern aiogram backend

<b>👨‍💻 Developer:</b>
GrandpaAcademy Team

<i>Built with ❤️ using simple Python!</i>
        """
        
        buttons = [
            [{"text": "🏠 Back to Start", "callback_data": "back_start"}],
            [{"text": "📋 Commands", "callback_data": "help_menu"}],
            [{"text": "❌ Close", "callback_data": "close_menu"}]
        ]
        
        kb = keyboard(buttons)
        await callback.message.edit_text(about_text.strip(), reply_markup=kb)
    
    @bot.callback("help_menu")
    async def help_menu_callback(bot_instance, callback):
        """Help menu callback"""
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

<i>Need more help? Contact support!</i>
        """
        
        buttons = [
            [{"text": "🏠 Back to Start", "callback_data": "back_start"}],
            [{"text": "❌ Close", "callback_data": "close_menu"}]
        ]
        
        kb = keyboard(buttons)
        await callback.message.edit_text(help_text.strip(), reply_markup=kb)
    
    @bot.callback("back_start")
    async def back_start_callback(bot_instance, callback):
        """Back to start callback"""
        user = callback.from_user
        user_name = user.first_name if user else "User"
        
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
        await callback.message.edit_text(welcome_text.strip(), reply_markup=kb)
    
    @bot.callback("close_menu")
    async def close_menu_callback(bot_instance, callback):
        """Close menu callback"""
        await callback.message.delete()

    @bot.callback("check_membership")
    async def check_membership_callback(bot_instance, callback):
        """Check force join membership callback"""
        user = callback.from_user

        if not user:
            await callback.answer("❌ Unable to verify membership")
            return

        # Check membership status
        is_member, not_joined = await force_join.check_user_membership(bot_instance, user.id)

        if is_member:
            # User has joined all required channels
            force_join.mark_user_checked(user.id)

            success_text = """
✅ <b>Membership Verified!</b>

Great! You've successfully joined all required channels.
You can now use all bot features!

<b>🚀 Available Commands:</b>
• /start - Welcome message
• /help - Show all commands
• /uid - Get your information

Thanks for joining our community! 🎉
            """

            buttons = [
                [{"text": "🏠 Start Bot", "callback_data": "back_start"}],
                [{"text": "📋 Commands", "callback_data": "help_menu"}]
            ]

            kb = keyboard(buttons)
            await callback.message.edit_text(success_text.strip(), reply_markup=kb)

        else:
            # User still needs to join some channels
            message_text, buttons = await force_join.get_force_join_message(not_joined)
            kb = keyboard(buttons)

            await callback.message.edit_text(
                f"❌ <b>Please join all required channels first!</b>\n\n{message_text}",
                reply_markup=kb
            )

        await callback.answer(
            "✅ Membership verified!" if is_member else "❌ Please join all channels first"
        )
