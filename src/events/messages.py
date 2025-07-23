"""
Message Events - Handle text messages for games and interactions
"""

from aiogram import types
import io
import logging

def register_events(dp):
    """Register message event handlers"""
    
    @dp.message()
    async def handle_messages(message: types.Message):
        """Handle all incoming text messages"""
        try:
            # Skip if no text
            if not message.text:
                return
            
            user = message.from_user
            chat_id = message.chat.id
            
            logging.info(f"Received message: '{message.text}' from user {user.id} in chat {chat_id}")
            
            # Handle number guessing game if message is a digit
            if message.text.isdigit():
                await handle_number_message(message, user, chat_id)
            else:
                await handle_text_message(message, user, chat_id)

        except Exception as e:
            logging.error(f"Error in message handler: {e}")
            import traceback
            traceback.print_exc()

async def handle_number_message(message, user, chat_id):
    """Handle numeric messages for guessing game"""
    try:
        # Import here to avoid circular imports
        from src.commands.games import active_games, create_guess_game_image
        from core import get_bot
        
        game_id = f"guess_{chat_id}_{user.id}"
        
        logging.info(f"Looking for game_id: {game_id}")
        logging.info(f"Active games: {list(active_games.keys())}")
        
        # Check if this is a guess game
        if game_id not in active_games:
            logging.info(f"No active game found for {game_id}")
            # Not in a game, just echo the number
            await message.reply(f"I received your number: {message.text}")
            return
        
        game = active_games[game_id]
        if game['type'] != 'guess':
            logging.info(f"Game type is {game['type']}, not 'guess'")
            return
        
        guess = int(message.text)
        target = game['target']
        
        logging.info(f"Processing guess {guess} for target {target}")
        
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
        
        bot = get_bot()
        if not bot:
            logging.error("Bot instance not found")
            return
        
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
            
    except Exception as e:
        logging.error(f"Error in number message handler: {e}")
        import traceback
        traceback.print_exc()

async def handle_text_message(message, user, chat_id):
    """Handle non-numeric text messages"""
    try:
        logging.info(f"Handling text message: '{message.text}'")
        
        # Simple echo response for testing
        if message.text.lower() in ['hello', 'hi', 'hey']:
            await message.reply(f"Hello {user.first_name}! 👋")
        elif message.text.lower() in ['how are you', 'how are you?']:
            await message.reply("I'm doing great! Thanks for asking! 😊")
        elif message.text.lower() in ['test', 'testing']:
            await message.reply("✅ Bot is working perfectly!")
        else:
            # Echo the message back
            await message.reply(f"You said: {message.text}")
            
    except Exception as e:
        logging.error(f"Error in text message handler: {e}")
        import traceback
        traceback.print_exc()
