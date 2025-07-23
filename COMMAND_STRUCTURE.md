# 🚀 TGbot - Simple Command Structure

## 📁 Current Command Files

### ✅ **Active Command Modules:**

1. **`src/commands/start.py`** - Welcome & introduction
2. **`src/commands/help.py`** - Command help system  
3. **`src/commands/uid.py`** - User information & utilities
4. **`src/commands/admin.py`** - Admin management commands
5. **`src/commands/example.py`** - Template & examples

### 🗑️ **Removed Files:**
- ~~`src/commands/basic.py`~~ - Split into separate files

---

## 🎯 Simple Syntax Structure

### **📝 Basic Command Template:**

```python
"""
Command Description
"""

from core import keyboard, is_admin, is_banned

def help():
    """Command help information - REQUIRED"""
    return {
        "name": "command_name",
        "description": "What this command does",
        "usage": "/command [args]",
        "aliases": ["cmd", "alias"],
        "category": "basic|admin|fun|utility",
        "examples": ["/command", "/command arg"],
        "permissions": ["all"] or ["admin"],
        "enabled": True
    }

async def my_command(bot, event):
    """Command function"""
    user = event.user
    chat = event.chat
    text = event.text
    
    # Your command logic here
    response = f"Hello {user.first_name}!"
    
    # Optional: Add buttons
    buttons = [
        [{"text": "Button", "callback_data": "action"}]
    ]
    kb = keyboard(buttons)
    
    await bot.send_message(event.chat.id, response, reply_markup=kb)

def register(handler):
    """Register commands - REQUIRED"""
    handler.add_command("mycommand", my_command, help())
```

---

## 📋 Available Commands

### **🏠 Basic Commands (`start.py`):**
- `/start` - Welcome message with interactive buttons

### **📖 Help System (`help.py`):**
- `/help` - Show all commands
- `/help <command>` - Detailed command help

### **🆔 User Info (`uid.py`):**
- `/uid` - User & chat information
- `/ping` - Bot response time
- `/about` - Bot information & features

### **👑 Admin Commands (`admin.py`):**
- `/ban` - Ban user from bot
- `/unban` - Unban user
- `/addadmin` - Add admin privileges
- `/stats` - Bot statistics
- `/reload` - Reload bot modules

### **🎮 Example Commands (`example.py`):**
- `/example` - Basic command demo
- `/demo <text>` - Command with arguments
- `/test` - Interactive buttons demo
- `/adminexample` - Admin-only command
- `/fun` - Random responses

---

## 🔧 Command Features

### **✅ Built-in Features:**
- **Auto user registration** - Users added to database automatically
- **Permission checks** - Admin/ban status checked automatically
- **Rate limiting** - Spam protection built-in
- **Error handling** - Graceful error management
- **Interactive buttons** - Easy keyboard creation
- **Help system** - Automatic help generation

### **🎨 Simple Syntax Benefits:**
- **No complex decorators** - Just simple functions
- **No router setup** - Automatic registration
- **No boilerplate** - Clean, readable code
- **Easy debugging** - Clear error messages
- **Fast development** - Add commands in seconds

---

## 📊 Bot Status

```
🤖 Bot Name: KOMI HUB 2
✅ SimpleBot initialized
✅ Commands loaded: 5 modules
✅ Total commands: 15+ commands
✅ Callbacks registered: 5 handlers
✅ Database: Working
✅ Permissions: Working
✅ Polling: Active
```

### **📈 Command Count:**
- **start.py**: 1 command (`/start`)
- **help.py**: 1 command (`/help`)
- **uid.py**: 3 commands (`/uid`, `/ping`, `/about`)
- **admin.py**: 5 commands (`/ban`, `/unban`, `/addadmin`, `/stats`, `/reload`)
- **example.py**: 5 commands (`/example`, `/demo`, `/test`, `/adminexample`, `/fun`)

**Total: 15 commands** across 5 modules

---

## 🚀 Adding New Commands

### **1. Create New File:**
```bash
touch src/commands/mycommands.py
```

### **2. Use Template:**
```python
from core import keyboard

def help():
    return {
        "name": "newcommand",
        "description": "My new command",
        "usage": "/newcommand",
        "category": "utility"
    }

async def new_command(bot, event):
    await bot.send_message(event.chat.id, "Hello from new command!")

def register(handler):
    handler.add_command("newcommand", new_command, help())
```

### **3. Restart Bot:**
```bash
python bot.py
```

**That's it! No complex setup needed!** 🎉

---

## 💡 Pro Tips

### **🔥 Best Practices:**
1. **One file per category** (admin, fun, utility, etc.)
2. **Clear function names** (`start_command`, `help_command`)
3. **Descriptive help info** - Users will see this
4. **Error handling** - Check for missing args
5. **Admin checks** - Use `is_admin()` for sensitive commands
6. **Interactive buttons** - Make commands engaging

### **⚡ Quick Commands:**
```python
# Simple response
await bot.send_message(event.chat.id, "Hello!")

# With buttons
buttons = [[{"text": "Click me", "callback_data": "action"}]]
kb = keyboard(buttons)
await bot.send_message(event.chat.id, "Hello!", reply_markup=kb)

# Admin check
if not is_admin(event.user.id):
    await bot.send_message(event.chat.id, "❌ Admin only!")
    return
```

### **🎯 Command Categories:**
- **basic** - Essential commands (start, help)
- **utility** - Useful tools (uid, ping, calc)
- **fun** - Entertainment (jokes, games)
- **admin** - Management (ban, stats)
- **group** - Group management
- **info** - Information commands

---

## 🎊 **Success! Clean Command Structure Created!**

**Your bot now has:**
- ✅ **Super simple syntax** - No complex aiogram code
- ✅ **Modular structure** - Easy to organize and maintain
- ✅ **15+ working commands** - Ready to use
- ✅ **Interactive buttons** - Engaging user experience
- ✅ **Admin system** - User management built-in
- ✅ **Help system** - Self-documenting commands
- ✅ **Example templates** - Easy to extend

**Ready to add more commands? Just follow the simple template!** 🚀
