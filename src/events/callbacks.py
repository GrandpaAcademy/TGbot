from core import get_bot, keyboard
from core.force_join import force_join
from PIL import Image, ImageDraw, ImageFont
import io
import random

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

    # Import game functions
    from src.commands.games import active_games, create_ttt_board_image, check_winner, is_board_full, get_ai_move

    @bot.callback("ttt_")
    async def ttt_game_callback(bot_instance, callback):
        """Handle tic-tac-toe game moves"""
        data = callback.data

        if data.startswith("ttt_new_"):
            # New game
            game_id = data.replace("ttt_new_", "")
            user_id = callback.from_user.id
            chat_id = callback.message.chat.id

            # Initialize new game
            board = [[' ' for _ in range(3)] for _ in range(3)]
            active_games[game_id] = {
                'board': board,
                'current_player': 'X',
                'user_id': user_id,
                'chat_id': chat_id,
                'vs_ai': True
            }

            # Create new board image
            img = create_ttt_board_image(board)
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)

            # Create buttons
            buttons = []
            for row in range(3):
                button_row = []
                for col in range(3):
                    button_row.append({
                        "text": "⬜",
                        "callback_data": f"ttt_{game_id}_{row}_{col}"
                    })
                buttons.append(button_row)

            buttons.append([
                {"text": "🔄 New Game", "callback_data": f"ttt_new_{game_id}"},
                {"text": "❌ Quit", "callback_data": f"ttt_quit_{game_id}"}
            ])

            kb = keyboard(buttons)

            caption = f"""
🎮 <b>Tic-Tac-Toe Game</b>

<b>Player:</b> {callback.from_user.first_name} (❌)
<b>Opponent:</b> AI Bot (⭕)

<b>Your turn!</b> Click any empty cell to make your move.

<i>Good luck! 🍀</i>
            """

            await callback.message.edit_media(
                media=callback.message.photo[-1],
                reply_markup=kb
            )
            await callback.message.edit_caption(caption.strip(), reply_markup=kb)

        elif data.startswith("ttt_quit_"):
            # Quit game
            game_id = data.replace("ttt_quit_", "")
            if game_id in active_games:
                del active_games[game_id]

            await callback.message.edit_caption(
                "🎮 <b>Game Ended</b>\n\nThanks for playing! Use /ttt to start a new game.",
                reply_markup=None
            )

        elif "_" in data and len(data.split("_")) >= 4:
            # Game move
            parts = data.split("_")
            if len(parts) >= 4:
                game_id = f"{parts[1]}_{parts[2]}"
                row, col = int(parts[3]), int(parts[4])

                if game_id not in active_games:
                    await callback.answer("❌ Game not found!")
                    return

                game = active_games[game_id]
                board = game['board']

                # Check if move is valid
                if board[row][col] != ' ':
                    await callback.answer("❌ Cell already taken!")
                    return

                # Make user move
                board[row][col] = 'X'

                # Check for winner
                winner, winning_line = check_winner(board)
                game_over = winner is not None or is_board_full(board)

                if not game_over:
                    # AI move
                    ai_move = get_ai_move(board)
                    if ai_move:
                        ai_row, ai_col = ai_move
                        board[ai_row][ai_col] = 'O'
                        winner, winning_line = check_winner(board)
                        game_over = winner is not None or is_board_full(board)

                # Create updated board image
                img = create_ttt_board_image(board, winner, winning_line)
                bio = io.BytesIO()
                img.save(bio, format='PNG')
                bio.seek(0)

                # Update buttons
                buttons = []
                for r in range(3):
                    button_row = []
                    for c in range(3):
                        if board[r][c] == ' ':
                            button_row.append({
                                "text": "⬜",
                                "callback_data": f"ttt_{game_id}_{r}_{c}"
                            })
                        elif board[r][c] == 'X':
                            button_row.append({
                                "text": "❌",
                                "callback_data": f"ttt_taken"
                            })
                        else:
                            button_row.append({
                                "text": "⭕",
                                "callback_data": f"ttt_taken"
                            })
                    buttons.append(button_row)

                buttons.append([
                    {"text": "🔄 New Game", "callback_data": f"ttt_new_{game_id}"},
                    {"text": "❌ Quit", "callback_data": f"ttt_quit_{game_id}"}
                ])

                kb = keyboard(buttons)

                # Create caption
                if winner == 'X':
                    caption = f"🎉 <b>You Win!</b>\n\n{callback.from_user.first_name} defeated the AI!"
                elif winner == 'O':
                    caption = f"🤖 <b>AI Wins!</b>\n\nBetter luck next time!"
                elif is_board_full(board):
                    caption = f"🤝 <b>It's a Tie!</b>\n\nGood game!"
                else:
                    caption = f"""
🎮 <b>Tic-Tac-Toe Game</b>

<b>Player:</b> {callback.from_user.first_name} (❌)
<b>Opponent:</b> AI Bot (⭕)

<b>Your turn!</b> Click any empty cell to make your move.
                    """

                # Send updated image
                await bot_instance.bot.edit_message_media(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                    media=callback.message.photo[-1]
                )
                await callback.message.edit_caption(caption.strip(), reply_markup=kb)

                if game_over:
                    # Clean up game
                    if game_id in active_games:
                        del active_games[game_id]

        await callback.answer()

    @bot.callback("rps_")
    async def rps_game_callback(bot_instance, callback):
        """Handle Rock Paper Scissors game"""
        data = callback.data

        if data.startswith("rps_new_"):
            # New game - just show the same interface
            user_id = int(data.replace("rps_new_", ""))

            # Create new RPS image (same as initial)
            from src.commands.games import rock_paper_scissors_command
            # Recreate the game interface
            await callback.answer("🔄 New game ready!")
            return

        elif "_" in data and len(data.split("_")) >= 3:
            # Game move
            parts = data.split("_")
            user_id = int(parts[1])
            user_choice = parts[2]

            if callback.from_user.id != user_id:
                await callback.answer("❌ This is not your game!")
                return

            # AI choice
            ai_choices = ["rock", "paper", "scissors"]
            ai_choice = random.choice(ai_choices)

            # Determine winner
            def get_winner(p1, p2):
                if p1 == p2:
                    return "tie"
                elif (p1 == "rock" and p2 == "scissors") or \
                     (p1 == "paper" and p2 == "rock") or \
                     (p1 == "scissors" and p2 == "paper"):
                    return "player"
                else:
                    return "ai"

            result = get_winner(user_choice, ai_choice)

            # Create result image
            width, height = 600, 500
            bg_color = (45, 45, 60)

            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)

            # Try to load fonts
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                text_font = ImageFont.load_default()

            # Header
            if result == "player":
                header_color = (100, 255, 100)
                result_text = "🎉 You Win!"
            elif result == "ai":
                header_color = (255, 100, 100)
                result_text = "🤖 AI Wins!"
            else:
                header_color = (255, 200, 100)
                result_text = "🤝 It's a Tie!"

            draw.rectangle([0, 0, width, 80], fill=header_color)
            draw.text((width//2 - 80, 25), result_text, font=title_font, fill=(255, 255, 255))

            # Choices display
            choice_emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
            choice_names = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}

            y_pos = 120
            draw.text((50, y_pos), f"👤 {callback.from_user.first_name}:", font=subtitle_font, fill=(255, 255, 255))
            draw.text((50, y_pos + 40), f"{choice_emojis[user_choice]} {choice_names[user_choice]}", font=title_font, fill=(100, 150, 255))

            draw.text((350, y_pos), "🤖 AI Bot:", font=subtitle_font, fill=(255, 255, 255))
            draw.text((350, y_pos + 40), f"{choice_emojis[ai_choice]} {choice_names[ai_choice]}", font=title_font, fill=(255, 100, 100))

            # VS
            draw.text((width//2 - 20, y_pos + 40), "VS", font=subtitle_font, fill=(255, 255, 255))

            # Result explanation
            y_pos += 120
            if result == "tie":
                explanation = "Both players chose the same!"
            elif result == "player":
                explanation = f"{choice_names[user_choice]} beats {choice_names[ai_choice]}!"
            else:
                explanation = f"{choice_names[ai_choice]} beats {choice_names[user_choice]}!"

            draw.text((50, y_pos), explanation, font=text_font, fill=(200, 200, 200))

            # Score suggestion
            y_pos += 50
            draw.text((50, y_pos), "🏆 Want to play again?", font=subtitle_font, fill=(255, 255, 255))

            # Convert to bytes
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)

            # Create buttons for new game
            buttons = [
                [
                    {"text": "🪨 Rock", "callback_data": f"rps_{user_id}_rock"},
                    {"text": "📄 Paper", "callback_data": f"rps_{user_id}_paper"},
                    {"text": "✂️ Scissors", "callback_data": f"rps_{user_id}_scissors"}
                ],
                [{"text": "🔄 New Game", "callback_data": f"rps_new_{user_id}"}]
            ]

            kb = keyboard(buttons)

            # Update message with result
            await bot_instance.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=callback.message.photo[-1]
            )

            caption = f"""
✂️ <b>Rock Paper Scissors - Result</b>

<b>{result_text}</b>

<b>Your choice:</b> {choice_emojis[user_choice]} {choice_names[user_choice]}
<b>AI choice:</b> {choice_emojis[ai_choice]} {choice_names[ai_choice]}

{explanation}

<i>Play again? 🎮</i>
            """

            await callback.message.edit_caption(caption.strip(), reply_markup=kb)

        await callback.answer()
