"""
Hot Reload System - Reload commands and events without restarting bot
"""

import logging
import importlib
import sys
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HotReloader:
    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}
        self.file_timestamps: Dict[str, float] = {}
    
    def reload_module(self, module_path: str) -> bool:
        """Reload a specific module"""
        try:
            # Get module name from path
            if module_path.endswith('.py'):
                module_path = module_path[:-3]
            
            module_name = module_path.replace('/', '.').replace('\\', '.')
            
            # Remove from sys.modules if exists
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            # Import the module
            module = importlib.import_module(module_name)
            
            # Store in loaded modules
            self.loaded_modules[module_name] = module
            
            logger.info(f"Successfully reloaded module: {module_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error reloading module {module_path}: {e}")
            return False
    
    def reload_commands(self, commands_dir: str = "src/commands") -> int:
        """Reload all command modules"""
        if not os.path.exists(commands_dir):
            logger.warning(f"Commands directory '{commands_dir}' not found")
            return 0
        
        reloaded_count = 0
        
        for filename in os.listdir(commands_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_path = f"{commands_dir}/{filename}"
                
                if self.reload_module(module_path.replace('/', '.')):
                    reloaded_count += 1
        
        logger.info(f"Reloaded {reloaded_count} command modules")
        return reloaded_count
    
    def reload_events(self, events_dir: str = "src/events") -> int:
        """Reload all event modules"""
        if not os.path.exists(events_dir):
            logger.warning(f"Events directory '{events_dir}' not found")
            return 0
        
        reloaded_count = 0
        
        for filename in os.listdir(events_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_path = f"{events_dir}/{filename}"
                
                if self.reload_module(module_path.replace('/', '.')):
                    reloaded_count += 1
        
        logger.info(f"Reloaded {reloaded_count} event modules")
        return reloaded_count
    
    def check_file_changes(self, directory: str) -> list:
        """Check for file changes in directory"""
        changed_files = []
        
        if not os.path.exists(directory):
            return changed_files
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    current_time = os.path.getmtime(file_path)
                    
                    if file_path in self.file_timestamps:
                        if current_time > self.file_timestamps[file_path]:
                            changed_files.append(file_path)
                    
                    self.file_timestamps[file_path] = current_time
        
        return changed_files
    
    def auto_reload_on_change(self) -> int:
        """Auto reload modules that have changed"""
        total_reloaded = 0
        
        # Check commands directory
        changed_commands = self.check_file_changes("src/commands")
        for file_path in changed_commands:
            if self.reload_module(file_path):
                total_reloaded += 1
        
        # Check events directory
        changed_events = self.check_file_changes("src/events")
        for file_path in changed_events:
            if self.reload_module(file_path):
                total_reloaded += 1
        
        if total_reloaded > 0:
            logger.info(f"Auto-reloaded {total_reloaded} modules")
        
        return total_reloaded
    
    def reload_all(self) -> Dict[str, int]:
        """Reload all modules"""
        results = {
            'commands': self.reload_commands(),
            'events': self.reload_events()
        }
        
        total = sum(results.values())
        logger.info(f"Reloaded {total} total modules")
        
        return results

# Global hot reloader instance
hot_reloader = HotReloader()

# Helper functions
def reload_commands() -> int:
    """Reload all commands"""
    return hot_reloader.reload_commands()

def reload_events() -> int:
    """Reload all events"""
    return hot_reloader.reload_events()

def reload_all() -> Dict[str, int]:
    """Reload everything"""
    return hot_reloader.reload_all()

def auto_reload() -> int:
    """Auto reload changed files"""
    return hot_reloader.auto_reload_on_change()
