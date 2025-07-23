"""
Member Events - Handle user join/leave with visual cards
"""

from core import get_bot
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import os

def register_events(dp):
    """Register member join/leave events"""
    bot = get_bot()
    
    if not bot:
        return

def create_welcome_card(user_name, user_username, chat_title, member_count, profile_photo_url=None):
    """Create a welcome card for new members"""
    # Card dimensions
    width, height = 800, 400
    
    # Colors
    bg_gradient_start = (45, 45, 45)
    bg_gradient_end = (25, 25, 25)
    accent_color = (100, 150, 255)
    text_color = (255, 255, 255)
    subtitle_color = (200, 200, 200)
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), bg_gradient_start)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        ratio = y / height
        r = int(bg_gradient_start[0] * (1 - ratio) + bg_gradient_end[0] * ratio)
        g = int(bg_gradient_start[1] * (1 - ratio) + bg_gradient_end[1] * ratio)
        b = int(bg_gradient_start[2] * (1 - ratio) + bg_gradient_end[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add decorative elements
    # Top accent bar
    draw.rectangle([0, 0, width, 8], fill=accent_color)
    
    # Welcome badge
    badge_x, badge_y = 50, 50
    badge_width, badge_height = 120, 40
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
        radius=20, fill=accent_color
    )
    
    # Try to load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
    
    # Draw welcome badge text
    draw.text((badge_x + 25, badge_y + 10), "WELCOME", font=badge_font, fill=(255, 255, 255))
    
    # Profile photo placeholder/circle
    photo_size = 100
    photo_x, photo_y = width - photo_size - 50, 50
    
    if profile_photo_url:
        try:
            # Download and process profile photo
            response = requests.get(profile_photo_url, timeout=5)
            if response.status_code == 200:
                profile_img = Image.open(io.BytesIO(response.content))
                profile_img = profile_img.resize((photo_size, photo_size))
                
                # Create circular mask
                mask = Image.new('L', (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, photo_size, photo_size], fill=255)
                
                # Apply mask to profile image
                profile_img.putalpha(mask)
                img.paste(profile_img, (photo_x, photo_y), profile_img)
            else:
                # Fallback to default avatar
                draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], 
                           fill=accent_color, outline=text_color, width=3)
                draw.text((photo_x + 35, photo_y + 35), "👤", font=title_font, fill=text_color)
        except:
            # Fallback to default avatar
            draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], 
                       fill=accent_color, outline=text_color, width=3)
            draw.text((photo_x + 35, photo_y + 35), "👤", font=title_font, fill=text_color)
    else:
        # Default avatar
        draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], 
                   fill=accent_color, outline=text_color, width=3)
        draw.text((photo_x + 35, photo_y + 35), "👤", font=title_font, fill=text_color)
    
    # Main welcome text
    welcome_text = f"Welcome to {chat_title}!"
    text_y = 120
    draw.text((50, text_y), welcome_text, font=title_font, fill=text_color)
    
    # User name
    name_text = f"👋 {user_name}"
    if user_username:
        name_text += f" (@{user_username})"
    
    text_y += 50
    draw.text((50, text_y), name_text, font=name_font, fill=accent_color)
    
    # Member count
    text_y += 40
    member_text = f"🎉 You are member #{member_count}"
    draw.text((50, text_y), member_text, font=subtitle_font, fill=subtitle_color)
    
    # Rules reminder
    text_y += 30
    rules_text = "📋 Please read the group rules and enjoy your stay!"
    draw.text((50, text_y), rules_text, font=subtitle_font, fill=subtitle_color)
    
    # Decorative bottom accent
    draw.rectangle([0, height - 8, width, height], fill=accent_color)
    
    return img

def create_goodbye_card(user_name, user_username, chat_title, member_count):
    """Create a goodbye card for leaving members"""
    # Card dimensions
    width, height = 800, 300
    
    # Colors (more muted for goodbye)
    bg_gradient_start = (60, 45, 45)
    bg_gradient_end = (40, 25, 25)
    accent_color = (255, 150, 100)
    text_color = (255, 255, 255)
    subtitle_color = (200, 200, 200)
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), bg_gradient_start)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        ratio = y / height
        r = int(bg_gradient_start[0] * (1 - ratio) + bg_gradient_end[0] * ratio)
        g = int(bg_gradient_start[1] * (1 - ratio) + bg_gradient_end[1] * ratio)
        b = int(bg_gradient_start[2] * (1 - ratio) + bg_gradient_end[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add decorative elements
    draw.rectangle([0, 0, width, 6], fill=accent_color)
    
    # Goodbye badge
    badge_x, badge_y = 50, 40
    badge_width, badge_height = 120, 35
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
        radius=18, fill=accent_color
    )
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
    
    # Draw goodbye badge text
    draw.text((badge_x + 20, badge_y + 8), "GOODBYE", font=badge_font, fill=(255, 255, 255))
    
    # Sad emoji
    emoji_x, emoji_y = width - 100, 40
    draw.text((emoji_x, emoji_y), "😢", font=title_font, fill=text_color)
    
    # Main goodbye text
    goodbye_text = f"Goodbye from {chat_title}"
    text_y = 100
    draw.text((50, text_y), goodbye_text, font=title_font, fill=text_color)
    
    # User name
    name_text = f"👋 {user_name}"
    if user_username:
        name_text += f" (@{user_username})"
    name_text += " left the group"
    
    text_y += 45
    draw.text((50, text_y), name_text, font=name_font, fill=accent_color)
    
    # Member count
    text_y += 35
    member_text = f"👥 {member_count} members remaining"
    draw.text((50, text_y), member_text, font=subtitle_font, fill=subtitle_color)
    
    # Farewell message
    text_y += 25
    farewell_text = "We hope to see you again soon! 💙"
    draw.text((50, text_y), farewell_text, font=subtitle_font, fill=subtitle_color)
    
    # Decorative bottom accent
    draw.rectangle([0, height - 6, width, height], fill=accent_color)
    
    return img

async def handle_new_member(bot, message):
    """Handle new member joining"""
    new_members = message.new_chat_members
    chat = message.chat
    
    for member in new_members:
        if member.is_bot:
            continue  # Skip bots
        
        # Get member count
        try:
            chat_info = await bot.bot.get_chat(chat.id)
            member_count = getattr(chat_info, 'member_count', 'Unknown')
        except:
            member_count = 'Unknown'
        
        # Get profile photo URL
        profile_photo_url = None
        try:
            photos = await bot.bot.get_user_profile_photos(member.id, limit=1)
            if photos.total_count > 0:
                photo = photos.photos[0][-1]  # Get largest photo
                file_info = await bot.bot.get_file(photo.file_id)
                profile_photo_url = f"https://api.telegram.org/file/bot{bot.bot.token}/{file_info.file_path}"
        except:
            pass
        
        # Create welcome card
        welcome_img = create_welcome_card(
            user_name=member.first_name or "New Member",
            user_username=member.username,
            chat_title=chat.title or "Group",
            member_count=member_count,
            profile_photo_url=profile_photo_url
        )
        
        # Convert to bytes
        bio = io.BytesIO()
        welcome_img.save(bio, format='PNG')
        bio.seek(0)
        
        # Send welcome card
        caption = f"""
🎉 <b>Welcome to {chat.title}!</b>

Hello {member.first_name}! We're glad to have you here.

<b>📋 Quick Tips:</b>
• Read the group rules
• Be respectful to everyone
• Have fun and enjoy your stay!

<i>Welcome aboard! 🚀</i>
        """
        
        await bot.bot.send_photo(
            chat.id,
            bio,
            caption=caption.strip(),
            parse_mode='HTML'
        )

async def handle_left_member(bot, message):
    """Handle member leaving"""
    left_member = message.left_chat_member
    chat = message.chat
    
    if left_member.is_bot:
        return  # Skip bots
    
    # Get member count
    try:
        chat_info = await bot.bot.get_chat(chat.id)
        member_count = getattr(chat_info, 'member_count', 'Unknown')
    except:
        member_count = 'Unknown'
    
    # Create goodbye card
    goodbye_img = create_goodbye_card(
        user_name=left_member.first_name or "Member",
        user_username=left_member.username,
        chat_title=chat.title or "Group",
        member_count=member_count
    )
    
    # Convert to bytes
    bio = io.BytesIO()
    goodbye_img.save(bio, format='PNG')
    bio.seek(0)
    
    # Send goodbye card
    caption = f"""
👋 <b>Farewell from {chat.title}</b>

{left_member.first_name} has left the group.

We hope to see you again soon! 💙
    """
    
    await bot.bot.send_photo(
        chat.id,
        bio,
        caption=caption.strip(),
        parse_mode='HTML'
    )
