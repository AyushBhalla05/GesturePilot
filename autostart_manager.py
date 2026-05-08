"""
GesturePilot - Phase 5: Auto-start Manager
Author: Your Name
Description: Manages Windows startup auto-start functionality
"""

import sys
import os
from pathlib import Path

try:
    import winreg
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False
    print("⚠️ winreg not available (not Windows)")

class AutoStartManager:
    """
    Manages Windows startup auto-start
    """
    
    def __init__(self, app_name="GesturePilot"):
        """
        Initialize auto-start manager
        
        Args:
            app_name (str): Application name for registry
        """
        self.app_name = app_name
        self.reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        if not REGISTRY_AVAILABLE:
            print("⚠️ Auto-start only available on Windows")
            return
        
        print("🚀 Auto-start Manager initialized")
    
    def enable(self):
        """
        Enable auto-start on Windows startup
        
        Returns:
            bool: Success status
        """
        if not REGISTRY_AVAILABLE:
            print("❌ Auto-start not available on this platform")
            return False
        
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                exe_path = sys.executable
            else:
                # Running as script
                exe_path = os.path.abspath(sys.argv[0])
                if exe_path.endswith('.py'):
                    # Convert to python command
                    python_exe = sys.executable
                    exe_path = f'"{python_exe}" "{exe_path}"'
            
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.reg_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set value
            winreg.SetValueEx(
                key,
                self.app_name,
                0,
                winreg.REG_SZ,
                exe_path
            )
            
            winreg.CloseKey(key)
            
            print(f"✅ Auto-start enabled: {exe_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to enable auto-start: {e}")
            return False
    
    def disable(self):
        """
        Disable auto-start
        
        Returns:
            bool: Success status
        """
        if not REGISTRY_AVAILABLE:
            print("❌ Auto-start not available on this platform")
            return False
        
        try:
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.reg_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Delete value
            winreg.DeleteValue(key, self.app_name)
            winreg.CloseKey(key)
            
            print("✅ Auto-start disabled")
            return True
            
        except FileNotFoundError:
            # Value doesn't exist
            print("ℹ️ Auto-start was not enabled")
            return True
            
        except Exception as e:
            print(f"❌ Failed to disable auto-start: {e}")
            return False
    
    def is_enabled(self):
        """
        Check if auto-start is currently enabled
        
        Returns:
            bool: True if enabled
        """
        if not REGISTRY_AVAILABLE:
            return False
        
        try:
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.reg_path,
                0,
                winreg.KEY_READ
            )
            
            # Try to read value
            value, _ = winreg.QueryValueEx(key, self.app_name)
            winreg.CloseKey(key)
            
            return True
            
        except FileNotFoundError:
            # Value doesn't exist
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking auto-start: {e}")
            return False
    
    def get_startup_path(self):
        """
        Get the path that would be added to startup
        
        Returns:
            str: Executable path
        """
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            return os.path.abspath(sys.argv[0])
    
    def toggle(self):
        """
        Toggle auto-start on/off
        
        Returns:
            bool: New state (True if now enabled)
        """
        if self.is_enabled():
            self.disable()
            return False
        else:
            self.enable()
            return True


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 TESTING AUTO-START MANAGER")
    print("=" * 50)
    
    manager = AutoStartManager("GesturePilot_Test")
    
    # Check current status
    print(f"\n📊 Current status: {'Enabled' if manager.is_enabled() else 'Disabled'}")
    print(f"📂 Startup path: {manager.get_startup_path()}")
    
    # Test enable
    print("\n🧪 Test 1: Enable auto-start")
    success = manager.enable()
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    print(f"   Status: {'Enabled' if manager.is_enabled() else 'Disabled'}")
    
    # Test disable
    print("\n🧪 Test 2: Disable auto-start")
    success = manager.disable()
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    print(f"   Status: {'Enabled' if manager.is_enabled() else 'Disabled'}")
    
    print("\n✅ Auto-start Manager tests completed!")
    print("\nNote: Check Windows Task Manager > Startup tab to verify")