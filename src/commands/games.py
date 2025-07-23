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

def register(handler):
    handler.add_command("ttt", ttt_command, help())
    handler.add_command("tictactoe", ttt_command, {"description": "Play tic-tac-toe game"})
