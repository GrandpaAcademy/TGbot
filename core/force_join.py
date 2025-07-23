"""
Force Join Module - Require users to join channels before using bot
"""

import logging
from .utils import load_config
from .database import db

logger = logging.getLogger(__name__)

class ForceJoin:
    def __init__(self):
        self.config = load_config()
        self.force_channels = self.config.get('force', {})
        self.enabled = bool(self.force_channels)
        
        if self.enabled:
            logger.info(f"Force join enabled for channels: {list(self.force_channels.values())}")
        else:
            logger.info("Force join disabled - no channels configured")
    
    async def check_user_membership(self, bot, user_id):
        """Check if user is member of all required channels"""
        if not self.enabled:
            return True, []
        
        not_joined = []
        
        for channel_type, channel_username in self.force_channels.items():
            try:
                # Get chat member status
                member = await bot.bot.get_chat_member(channel_username, user_id)
                
                # Check if user is member (not left or kicked)
                if member.status in ['left', 'kicked']:
                    not_joined.append({
                        'type': channel_type,
                        'username': channel_username,
                        'url': f"https://t.me/{channel_username.replace('@', '')}"
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to check membership for {channel_username}: {e}")
                # If we can't check, assume user needs to join
                not_joined.append({
                    'type': channel_type,
                    'username': channel_username,
                    'url': f"https://t.me/{channel_username.replace('@', '')}"
                })
        
        return len(not_joined) == 0, not_joined
    
    async def get_force_join_message(self, not_joined_channels):
        """Generate force join message with buttons"""
        if not not_joined_channels:
            return None, None
        
        text = """
🔒 <b>Join Required Channels</b>

To use this bot, you must join our official channels first:

<b>📢 Required Channels:</b>
        """
        
        buttons = []
        
        for channel in not_joined_channels:
            channel_name = channel['username'].replace('@', '')
            text += f"• {channel['username']} - {channel['type'].title()}\n"
            
            buttons.append([{
                "text": f"📢 Join {channel['type'].title()}",
                "url": channel['url']
            }])
        
        text += """

<b>📋 Instructions:</b>
1. Click the buttons above to join channels
2. Click "✅ Check Membership" after joining
3. Start using the bot!

<i>This helps us provide better support and updates! 🚀</i>
        """
        
        # Add check membership button
        buttons.append([{
            "text": "✅ Check Membership",
            "callback_data": "check_membership"
        }])
        
        return text.strip(), buttons
    
    def mark_user_checked(self, user_id):
        """Mark user as having passed force join check"""
        try:
            # Update user record to show they've passed force join
            db.execute(
                "UPDATE users SET force_join_passed = 1 WHERE user_id = ?",
                (user_id,)
            )
            logger.info(f"User {user_id} passed force join check")
        except Exception as e:
            logger.error(f"Failed to mark user {user_id} as force join passed: {e}")
    
    def has_user_passed(self, user_id):
        """Check if user has already passed force join check"""
        try:
            result = db.execute(
                "SELECT force_join_passed FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            
            return result and result[0] == 1
        except Exception as e:
            logger.error(f"Failed to check force join status for user {user_id}: {e}")
            return False
    
    async def enforce_force_join(self, bot, event):
        """
        Enforce force join requirement
        Returns: (allowed, message_text, buttons)
        """
        if not self.enabled:
            return True, None, None
        
        user = event.user
        if not user:
            return True, None, None
        
        user_id = user.id
        
        # Check if user has already passed (to avoid repeated API calls)
        if self.has_user_passed(user_id):
            return True, None, None
        
        # Check current membership status
        is_member, not_joined = await self.check_user_membership(bot, user_id)
        
        if is_member:
            # User is now a member, mark as passed
            self.mark_user_checked(user_id)
            return True, None, None
        
        # User needs to join channels
        message_text, buttons = await self.get_force_join_message(not_joined)
        return False, message_text, buttons

# Global force join instance
force_join = ForceJoin()

async def check_force_join(bot, event):
    """
    Decorator function to check force join requirement
    Returns True if user can proceed, False if blocked
    """
    return await force_join.enforce_force_join(bot, event)

def is_force_join_enabled():
    """Check if force join is enabled"""
    return force_join.enabled

def get_force_channels():
    """Get list of force join channels"""
    return force_join.force_channels
