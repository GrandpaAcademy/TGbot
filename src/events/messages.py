"""
Message Events - Handle text messages for games and interactions
"""

from core import get_bot
from PIL import Image, ImageDraw, ImageFont
import io

def register_events(dp):
    """Register message event handlers"""
    bot = get_bot()
    
    if not bot:
        return

    @bot.dp.message()
    async def handle_messages(message):
        """Handle all incoming text messages"""
        # Import here to avoid circular imports
        from src.commands.games import active_games, create_guess_game_image
        
        # Skip if no text or not a digit
        if not message.text or not message.text.isdigit():
            return
        
        user = message.from_user
        chat_id = message.chat.id
        game_id = f"guess_{chat_id}_{user.id}"
        
        # Check if this is a guess game
        if game_id not in active_games:
            return
        
        game = active_games[game_id]
        if game['type'] != 'guess':
            return
        
        guess = int(message.text)
        target = game['target']
        
        # Validate guess range
        if guess < 1 or guess > 100:
            await message.reply("❌ Please guess a number between 1 and 100!")
            return
        
        # Check if already guessed
        if guess in game['attempts']:
            await message.reply("🔄 You already guessed that number! Try a different one.")
            return
        
        # Process guess
        game['attempts'].append(guess)
        
        if guess == target:
            # Won!
            hint = "🎉 Correct! You won!"
            game['hints'].append(hint)
            
            # Create winning image
            img = create_guess_game_image(
                game['attempts'], game['hints'], (1, 100),
                game_over=True, won=True
            )
            
            # Send result
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            
            caption = f"""
🎉 <b>Congratulations {user.first_name}!</b>

You found the number <b>{target}</b> in {len(game['attempts'])} attempts!

<b>🏆 Game Statistics:</b>
• Target Number: {target}
• Your Attempts: {len(game['attempts'])}/10
• Success Rate: {(1/len(game['attempts'])*100):.1f}%

<i>Excellent guessing! 🌟</i>
            """
            
            await bot.bot.send_photo(
                chat_id, bio, caption=caption.strip(), parse_mode='HTML'
            )
            
            # Clean up game
            del active_games[game_id]
            
        elif len(game['attempts']) >= game['max_attempts']:
            # Lost!
            hint = f"💔 Game over! The number was {target}"
            game['hints'].append(hint)
            
            # Create losing image
            img = create_guess_game_image(
                game['attempts'], game['hints'], (1, 100),
                game_over=True, won=False
            )
            
            # Send result
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            
            caption = f"""
💔 <b>Game Over, {user.first_name}!</b>

The number was <b>{target}</b>.
You used all 10 attempts.

<b>📊 Your Attempts:</b>
{', '.join(map(str, game['attempts']))}

<i>Better luck next time! Use /guess to try again. 🎯</i>
            """
            
            await bot.bot.send_photo(
                chat_id, bio, caption=caption.strip(), parse_mode='HTML'
            )
            
            # Clean up game
            del active_games[game_id]
            
        else:
            # Continue game
            if guess < target:
                hint = "📈 Too low! Try higher"
            else:
                hint = "📉 Too high! Try lower"
            
            game['hints'].append(hint)
            
            # Create updated image
            img = create_guess_game_image(
                game['attempts'], game['hints'], (1, 100)
            )
            
            # Send update
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            
            remaining = game['max_attempts'] - len(game['attempts'])
            caption = f"""
🎯 <b>Keep Guessing, {user.first_name}!</b>

<b>Your guess:</b> {guess}
<b>Hint:</b> {hint}
<b>Attempts left:</b> {remaining}

<i>You're getting closer! 🎲</i>
            """
            
            await bot.bot.send_photo(
                chat_id, bio, caption=caption.strip(), parse_mode='HTML'
            )
