# 🤖 TGbot - Simple Telegram Bot

**Clean, readable code with super simple syntax!**

## 🚀 Features

- **Super Simple Syntax** - No complex aiogram boilerplate
- **Clean Code Structure** - Organized and maintainable
- **Easy to Extend** - Add commands in seconds
- **Modern Backend** - Powered by aiogram 3.x
- **User Management** - Built-in database and permissions
- **Hot Reload** - Update code without restarting

## 📦 Installation

<b>For termux </b>
```bash
git clone https://github.com/tgbot/komi-hub.git
cd komi-hub
pip install -r requirements.txt
python bot.py
```
<b>For windows</b>
```bash
git clone https://github.com/tgbot/komi-hub.git
cd komi-hub
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```
<b> For linux</b>
```bash
git clone https://github.com/tgbot/komi-hub.git
cd komi-hub
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

## 📁 Project Structure

```
├── bot.py                 # Main bot file
├── config.json           # Bot configuration
├── requirements.txt      # Dependencies
├── core/                 # Core framework
│   ├── __init__.py
│   ├── translator.py     # Simple syntax translator
│   ├── database.py       # User database
│   ├── permissions.py    # Admin/ban system
│   ├── command_handler.py
│   ├── hot_reload.py
│   └── utils.py
├── src/
│   ├── commands/         # Bot commands
│   │   └── basic.py      # Basic commands
│   └── events/           # Event handlers
│       └── callbacks.py  # Callback handlers
```

## 🎯 Simple Syntax Examples

### Creating Commands

```python
from core import keyboard

def help():
    return {
        "name": "start",
        "description": "Start the bot",
        "usage": "/start",
        "category": "basic"
    }

async def start_command(bot, event):
    """Simple start command"""
    user_name = event.user.first_name if event.user else "User"
    
    text = f"🤖 Welcome {user_name}!"
    
    buttons = [
        [{"text": "🆔 Get ID", "callback_data": "get_uid"}],
        [{"text": "❌ Close", "callback_data": "close"}]
    ]
    
    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, text, reply_markup=kb)

def register(handler):
    """Register commands"""
    handler.add_command("start", start_command, help())
```

### Creating Callbacks

```python
from core import get_bot

def register_events(dp):
    """Register callback events"""
    bot = get_bot()
    
    @bot.callback("get_uid")
    async def get_uid_callback(bot_instance, callback):
        user = callback.from_user
        text = f"🆔 Your ID: <code>{user.id}</code>"
        await callback.message.edit_text(text)
```

## 🔧 Configuration

Edit `config.json`:

```json
{
    "token": "YOUR_BOT_TOKEN_HERE",
    "bot_name": "KOMI HUB 2",
    "admins": [1234567890],
    "features": {
        "welcome_messages": true,
        "admin_commands": true,
        "hot_reload": true
    }
}
```

## 🔧 Command Structure

===================================

<b> [READ DOCS]("./COMMAND_STRUCTURE.md") </b>

===================================
## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure bot:**
   - Edit `config.json`
   - Add your bot token

3. **Run bot:**
   ```bash
   python bot.py
   ```

## 📝 Adding New Commands

1. Create a new file in `src/commands/`
2. Use the simple syntax format
3. Register commands with `handler.add_command()`
4. Restart bot or use hot reload

## 🎨 Simple vs Complex

### ❌ Complex aiogram syntax:
```python
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Button", callback_data="data")]
    ])
    await message.reply("Hello!", reply_markup=keyboard)
```

### ✅ Simple syntax:
```python
async def start_command(bot, event):
    buttons = [[{"text": "Button", "callback_data": "data"}]]
    kb = keyboard(buttons)
    await bot.send_message(event.chat.id, "Hello!", reply_markup=kb)

def register(handler):
    handler.add_command("start", start_command, {"description": "Start command"})
```

## 🛠️ Core Features

- **Database**: Automatic user management
- **Permissions**: Admin/ban system built-in
- **Rate Limiting**: Prevent spam
- **Hot Reload**: Update code without restart
- **Event System**: Handle user joins/leaves
- **Callback Handlers**: Interactive buttons

## 📊 Bot Status

- **Framework**: aiogram 3.x with simple syntax
- **Database**: SQLite (built-in)
- **Language**: Python 3.12+
- **Architecture**: Modular and clean

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Use the simple syntax format
4. Submit pull request

## 📄 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ by GrandpaAcademy Team**

*Making Telegram bots simple and fun!* 🚀
