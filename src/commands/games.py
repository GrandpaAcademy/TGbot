"""
Games Commands - Fun games with visual responses
"""

from core import keyboard, is_admin
from PIL import Image, ImageDraw, ImageFont
import io
import random
import json
import os

# Game storage (in production, use database)
active_games = {}

def help():
    """Command help information"""
    return {
        "name": "games",
        "description": "Fun games with visual responses",
        "usage": "/ttt, /tictactoe",
        "aliases": ["games", "play", "fun"],
        "category": "fun",
        "examples": [
            "/ttt",
            "/tictactoe"
        ],
        "permissions": ["all"],
        "enabled": True
    }

def create_ttt_board_image(board, winner=None, winning_line=None):
    """Create a visual tic-tac-toe board using Pillow"""
    # Board dimensions
    size = 600
    cell_size = size // 3
    line_width = 8
    
    # Colors
    bg_color = (45, 45, 45)  # Dark gray
    line_color = (255, 255, 255)  # White
    x_color = (255, 100, 100)  # Red
    o_color = (100, 150, 255)  # Blue
    win_color = (50, 255, 50)  # Green
    
    # Create image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw grid lines
    for i in range(1, 3):
        # Vertical lines
        x = i * cell_size
        draw.line([(x, 0), (x, size)], fill=line_color, width=line_width)
        # Horizontal lines
        y = i * cell_size
        draw.line([(0, y), (size, y)], fill=line_color, width=line_width)
    
    # Draw X's and O's
    margin = 40
    for row in range(3):
        for col in range(3):
            cell_value = board[row][col]
            if cell_value != ' ':
                x1 = col * cell_size + margin
                y1 = row * cell_size + margin
                x2 = (col + 1) * cell_size - margin
                y2 = (row + 1) * cell_size - margin
                
                color = x_color if cell_value == 'X' else o_color
                
                if cell_value == 'X':
                    # Draw X
                    draw.line([(x1, y1), (x2, y2)], fill=color, width=12)
                    draw.line([(x1, y2), (x2, y1)], fill=color, width=12)
                else:
                    # Draw O
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    radius = (x2 - x1) // 2 - 10
                    draw.ellipse([center_x - radius, center_y - radius, 
                                center_x + radius, center_y + radius], 
                               outline=color, width=12)
    
    # Highlight winning line
    if winner and winning_line:
        start_row, start_col, end_row, end_col = winning_line
        start_x = start_col * cell_size + cell_size // 2
        start_y = start_row * cell_size + cell_size // 2
        end_x = end_col * cell_size + cell_size // 2
        end_y = end_row * cell_size + cell_size // 2
        
        draw.line([(start_x, start_y), (end_x, end_y)], fill=win_color, width=15)
    
    return img

def check_winner(board):
    """Check if there's a winner and return winner + winning line"""
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            return board[row][0], (row, 0, row, 2)
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col], (0, col, 2, col)
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0], (0, 0, 2, 2)
    
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2], (0, 2, 2, 0)
    
    return None, None

def is_board_full(board):
    """Check if board is full"""
    for row in board:
        if ' ' in row:
            return False
    return True

def get_ai_move(board):
    """Simple AI move - random available position"""
    available = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                available.append((row, col))
    
    return random.choice(available) if available else None

async def ttt_command(bot, event):
    """Start a new tic-tac-toe game"""
    user = event.user
    chat_id = event.chat.id
    
    # Initialize new game
    game_id = f"{chat_id}_{user.id}"
    board = [[' ' for _ in range(3)] for _ in range(3)]
    
    active_games[game_id] = {
        'board': board,
        'current_player': 'X',  # User is X
        'user_id': user.id,
        'chat_id': chat_id,
        'vs_ai': True
    }
    
    # Create board image
    img = create_ttt_board_image(board)
    
    # Convert to bytes
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    
    # Create game buttons
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

<b>Player:</b> {user.first_name} (❌)
<b>Opponent:</b> AI Bot (⭕)

<b>Your turn!</b> Click any empty cell to make your move.

<i>Good luck! 🍀</i>
    """
    
    # Send game image with buttons
    await bot.bot.send_photo(
        chat_id,
        bio,
        caption=caption.strip(),
        reply_markup=kb,
        parse_mode='HTML'
    )

def create_guess_game_image(attempts, hints, target_range=(1, 100), game_over=False, won=False):
    """Create a visual number guessing game board"""
    width, height = 800, 600

    # Colors
    bg_color = (30, 30, 40)
    header_color = (100, 150, 255)
    text_color = (255, 255, 255)
    hint_color = (255, 200, 100)
    success_color = (100, 255, 100)
    fail_color = (255, 100, 100)

    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        title_font = ImageFont.truetype("./assets/fonts/DejaVuSans-Bold.ttf", 32)
        subtitle_font = ImageFont.truetype("./assets/fonts/DejaVuSans-Bold.ttf", 24)
        text_font = ImageFont.truetype("./assets/fonts/DejaVuSans.ttf", 18)
        hint_font = ImageFont.truetype("./assets/fonts/DejaVuSans-Bold.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        hint_font = ImageFont.load_default()

    # Header
    draw.rectangle([0, 0, width, 80], fill=header_color)
    draw.text((width//2 - 150, 25), "🎯 Number Guessing Game", font=title_font, fill=(255, 255, 255))

    # Game info
    y_pos = 100
    range_text = f"🎲 Range: {target_range[0]} - {target_range[1]}"
    draw.text((50, y_pos), range_text, font=subtitle_font, fill=text_color)

    attempts_text = f"🎯 Attempts: {len(attempts)}/10"
    draw.text((width - 200, y_pos), attempts_text, font=subtitle_font, fill=text_color)

    # Attempts history
    y_pos += 60
    draw.text((50, y_pos), "📝 Your Attempts:", font=subtitle_font, fill=text_color)

    y_pos += 40
    for i, (guess, hint) in enumerate(zip(attempts, hints)):
        if i >= 8:  # Limit display to 8 attempts
            break

        attempt_text = f"{i+1}. {guess}"
        hint_text = hint

        # Color based on hint
        if "correct" in hint.lower() or "won" in hint.lower():
            color = success_color
        elif "higher" in hint.lower() or "lower" in hint.lower():
            color = hint_color
        else:
            color = text_color

        draw.text((70, y_pos), attempt_text, font=text_font, fill=color)
        draw.text((150, y_pos), f"→ {hint_text}", font=hint_font, fill=color)
        y_pos += 30

    # Game status
    if game_over:
        y_pos += 20
        if won:
            status_text = "🎉 Congratulations! You won!"
            status_color = success_color
        else:
            status_text = "💔 Game Over! Better luck next time!"
            status_color = fail_color

        draw.text((50, y_pos), status_text, font=subtitle_font, fill=status_color)
    else:
        y_pos += 20
        status_text = "🤔 Keep guessing! You can do it!"
        draw.text((50, y_pos), status_text, font=subtitle_font, fill=hint_color)

    # Instructions
    y_pos = height - 100
    draw.rectangle([0, y_pos - 10, width, height], fill=(20, 20, 30))
    draw.text((50, y_pos), "💡 Instructions:", font=subtitle_font, fill=text_color)
    draw.text((50, y_pos + 30), "• Type a number to make your guess", font=text_font, fill=text_color)
    draw.text((50, y_pos + 50), "• You have 10 attempts to find the number", font=text_font, fill=text_color)

    return img

async def guess_command(bot, event):
    """Start a number guessing game"""
    user = event.user
    chat_id = event.chat.id

    # Initialize new game
    game_id = f"guess_{chat_id}_{user.id}"
    target_number = random.randint(1, 100)

    active_games[game_id] = {
        'type': 'guess',
        'target': target_number,
        'attempts': [],
        'hints': [],
        'user_id': user.id,
        'chat_id': chat_id,
        'max_attempts': 10
    }

    # Create game image
    img = create_guess_game_image([], [], (1, 100))

    # Convert to bytes
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)

    caption = f"""
🎯 <b>Number Guessing Game Started!</b>

<b>Player:</b> {user.first_name}
<b>Range:</b> 1 - 100
<b>Attempts:</b> 10

I'm thinking of a number between 1 and 100.
Can you guess what it is?

<b>How to play:</b>
• Just type any number between 1-100
• I'll tell you if it's higher or lower
• You have 10 attempts to win!

<i>Good luck! 🍀</i>
    """

    # Send game image
    await bot.bot.send_photo(
        chat_id,
        bio,
        caption=caption.strip(),
        parse_mode='HTML'
    )

async def rock_paper_scissors_command(bot, event):
    """Play Rock Paper Scissors with visual results"""
    user = event.user

    # Create RPS game image
    width, height = 600, 400
    bg_color = (45, 45, 60)

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        title_font = ImageFont.truetype("./assets/fonts/DejaVuSans-Bold.ttf", 28)
        text_font = ImageFont.truetype("./assets/fonts/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Header
    draw.rectangle([0, 0, width, 60], fill=(100, 150, 255))
    draw.text((width//2 - 120, 20), "✂️ Rock Paper Scissors", font=title_font, fill=(255, 255, 255))

    # Instructions
    y_pos = 100
    draw.text((50, y_pos), f"🎮 Player: {user.first_name}", font=title_font, fill=(255, 255, 255))
    y_pos += 50
    draw.text((50, y_pos), "Choose your move:", font=text_font, fill=(200, 200, 200))

    # Choices display
    y_pos += 60
    choices = [
        ("🪨", "Rock", "Strong against Scissors"),
        ("📄", "Paper", "Strong against Rock"),
        ("✂️", "Scissors", "Strong against Paper")
    ]

    for emoji, name, desc in choices:
        draw.text((50, y_pos), f"{emoji} {name}", font=title_font, fill=(255, 255, 255))
        draw.text((200, y_pos + 5), f"- {desc}", font=text_font, fill=(150, 150, 150))
        y_pos += 40

    # Convert to bytes
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)

    # Create buttons
    buttons = [
        [
            {"text": "🪨 Rock", "callback_data": f"rps_{user.id}_rock"},
            {"text": "📄 Paper", "callback_data": f"rps_{user.id}_paper"},
            {"text": "✂️ Scissors", "callback_data": f"rps_{user.id}_scissors"}
        ],
        [{"text": "🔄 New Game", "callback_data": f"rps_new_{user.id}"}]
    ]

    kb = keyboard(buttons)

    caption = f"""
✂️ <b>Rock Paper Scissors</b>

<b>Player:</b> {user.first_name}
<b>Opponent:</b> AI Bot

Choose your move and let's see who wins!

<b>Rules:</b>
• Rock beats Scissors
• Paper beats Rock
• Scissors beats Paper

<i>May the best player win! 🏆</i>
    """

    await bot.bot.send_photo(
        event.chat.id,
        bio,
        caption=caption.strip(),
        reply_markup=kb,
        parse_mode='HTML'
    )

def register(handler):
    handler.add_command("ttt", ttt_command, help())
    handler.add_command("tictactoe", ttt_command, {"description": "Play tic-tac-toe game"})
    handler.add_command("guess", guess_command, {"description": "Number guessing game"})
    handler.add_command("rps", rock_paper_scissors_command, {"description": "Rock Paper Scissors game"})
