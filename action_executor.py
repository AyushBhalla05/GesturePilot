"""
GesturePilot - Phase 3: Action Executor
Author: Your Name
Description: Executes actions based on recognized gestures
"""

import webbrowser
import time
from system_controller import SystemController
from voice_feedback import VoiceFeedback

try:
    import pyautogui
    BROWSER_CONTROL_AVAILABLE = True
except ImportError:
    BROWSER_CONTROL_AVAILABLE = False

class ActionExecutor:
    """
    Executes actions triggered by gestures
    """
    
    def __init__(self, voice_enabled=True):
        """
        Initialize action executor
        
        Args:
            voice_enabled (bool): Enable voice feedback
        """
        print("🎬 Action Executor initializing...")
        
        # Initialize components
        self.system = SystemController()
        self.voice = VoiceFeedback(enabled=voice_enabled)
        
        # Action history
        self.action_history = []
        self.max_history = 100
        
        # Action statistics
        self.action_stats = {}
        
        print("✅ Action Executor initialized")
    
    def execute(self, action_name, params=None):
        """
        Execute an action
        
        Args:
            action_name (str): Action identifier
            params (dict, optional): Action parameters
            
        Returns:
            bool: Success status
        """
        print(f"\n⚡ Executing: {action_name}")
        
        # Record action
        self._record_action(action_name)
        
        # Announce action
        self.voice.announce_action(action_name)
        
        # Execute action
        success = False
        
        try:
            # Browser actions
            if action_name == 'open_youtube':
                success = self.open_youtube()
            elif action_name == 'browser_new_tab':
                success = self.browser_new_tab()
            elif action_name == 'browser_close_tab':
                success = self.browser_close_tab()
            
            # Media control
            elif action_name == 'music_play_pause':
                success = self.system.media_play_pause()
            elif action_name == 'music_next':
                success = self.system.media_next()
            elif action_name == 'music_previous':
                success = self.system.media_previous()
            
            # Volume control
            elif action_name == 'volume_up':
                success = self.system.volume_up()
            elif action_name == 'volume_down':
                success = self.system.volume_down()
            elif action_name == 'volume_mute':
                success = self.system.volume_mute()
            
            # Brightness control
            elif action_name == 'brightness_up':
                success = self.system.brightness_up()
            elif action_name == 'brightness_down':
                success = self.system.brightness_down()
            
            # Screenshot
            elif action_name == 'take_screenshot':
                success = self.system.take_screenshot()
            
            # Application launch
            elif action_name == 'open_calculator':
                success = self.system.open_calculator()
            elif action_name == 'open_notepad':
                success = self.system.open_notepad()
            
            # Window management
            elif action_name == 'minimize_all':
                success = self.system.minimize_all_windows()
            elif action_name == 'alt_tab':
                success = self.system.alt_tab()
            
            # Stop/Cancel
            elif action_name == 'stop_action':
                success = self.stop_action()
            
            else:
                print(f"⚠️ Unknown action: {action_name}")
                success = False
            
            # Log result
            if success:
                print(f"✅ Action completed: {action_name}")
            else:
                print(f"❌ Action failed: {action_name}")
            
            return success
            
        except Exception as e:
            print(f"❌ Action execution error: {e}")
            self.voice.announce_error("Action failed")
            return False
    
    # ========== BROWSER ACTIONS ==========
    
    def open_youtube(self):
        """Open YouTube in browser"""
        try:
            webbrowser.open('https://www.youtube.com')
            return True
        except Exception as e:
            print(f"❌ Failed to open YouTube: {e}")
            return False
    
    def open_url(self, url):
        """
        Open URL in browser
        
        Args:
            url (str): URL to open
        """
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"❌ Failed to open URL: {e}")
            return False
    
    def browser_new_tab(self):
        """Open new browser tab (Ctrl+T)"""
        if BROWSER_CONTROL_AVAILABLE:
            try:
                pyautogui.hotkey('ctrl', 't')
                return True
            except:
                return False
        return False
    
    def browser_close_tab(self):
        """Close current browser tab (Ctrl+W)"""
        if BROWSER_CONTROL_AVAILABLE:
            try:
                pyautogui.hotkey('ctrl', 'w')
                return True
            except:
                return False
        return False
    
    def browser_refresh(self):
        """Refresh browser (F5)"""
        if BROWSER_CONTROL_AVAILABLE:
            try:
                pyautogui.press('f5')
                return True
            except:
                return False
        return False
    
    def browser_back(self):
        """Browser back (Alt+Left)"""
        if BROWSER_CONTROL_AVAILABLE:
            try:
                pyautogui.hotkey('alt', 'left')
                return True
            except:
                return False
        return False
    
    def browser_forward(self):
        """Browser forward (Alt+Right)"""
        if BROWSER_CONTROL_AVAILABLE:
            try:
                pyautogui.hotkey('alt', 'right')
                return True
            except:
                return False
        return False
    
    # ========== SPECIAL ACTIONS ==========
    
    def stop_action(self):
        """Stop current action"""
        print("🛑 Stop signal received")
        return True
    
    # ========== ACTION TRACKING ==========
    
    def _record_action(self, action_name):
        """
        Record action in history
        
        Args:
            action_name (str): Action name
        """
        from datetime import datetime
        
        record = {
            'action': action_name,
            'timestamp': datetime.now().isoformat(),
            'success': True
        }
        
        self.action_history.append(record)
        
        # Maintain max history
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)
        
        # Update statistics
        if action_name not in self.action_stats:
            self.action_stats[action_name] = 0
        self.action_stats[action_name] += 1
    
    def get_action_history(self, limit=10):
        """
        Get recent action history
        
        Args:
            limit (int): Number of recent actions
            
        Returns:
            list: Recent actions
        """
        return self.action_history[-limit:]
    
    def get_action_statistics(self):
        """
        Get action statistics
        
        Returns:
            dict: Action counts
        """
        return self.action_stats.copy()
    
    def clear_history(self):
        """Clear action history"""
        self.action_history.clear()
        self.action_stats.clear()
        print("🗑️ Action history cleared")
    
    # ========== VOICE CONTROL ==========
    
    def set_voice_enabled(self, enabled):
        """
        Enable/disable voice feedback
        
        Args:
            enabled (bool): Enable state
        """
        self.voice.set_enabled(enabled)
    
    def is_voice_enabled(self):
        """Check if voice is enabled"""
        return self.voice.is_enabled()


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🎬 TESTING ACTION EXECUTOR")
    print("=" * 50)
    
    executor = ActionExecutor(voice_enabled=True)
    
    print("\n🧪 Test 1: Browser action (YouTube)")
    print("   (Will open YouTube in 3 seconds...)")
    time.sleep(3)
    executor.execute('open_youtube')
    
    print("\n🧪 Test 2: Volume control")
    print("   Testing volume up...")
    executor.execute('volume_up')
    
    print("\n🧪 Test 3: Action history")
    history = executor.get_action_history()
    print(f"   Recent actions: {len(history)}")
    for action in history:
        print(f"   - {action['action']} at {action['timestamp']}")
    
    print("\n🧪 Test 4: Statistics")
    stats = executor.get_action_statistics()
    print(f"   Action statistics:")
    for action, count in stats.items():
        print(f"   - {action}: {count} times")
    
    print("\n✅ Action Executor tests completed!")
    print("\nNote: Some actions require user interaction to verify")