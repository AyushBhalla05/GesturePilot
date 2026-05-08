"""
GesturePilot - Phase 3: System Controller
Author: Your Name
Description: Controls system functions like volume, brightness, apps
"""

import os
import sys
import subprocess
import platform

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ pyautogui not installed")

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import cast, POINTER
    VOLUME_CONTROL_AVAILABLE = True
except ImportError:
    VOLUME_CONTROL_AVAILABLE = False
    print("⚠️ Volume control not available")
except Exception as e:
    VOLUME_CONTROL_AVAILABLE = False
    print(f"⚠️ pycaw import error: {e}")

try:
    import screen_brightness_control as sbc
    BRIGHTNESS_CONTROL_AVAILABLE = True
except ImportError:
    BRIGHTNESS_CONTROL_AVAILABLE = False
    print("⚠️ Brightness control not available (install screen-brightness-control)")

class SystemController:
    """
    Controls system functions: volume, brightness, apps, keyboard shortcuts
    """
    
    def __init__(self):
        """Initialize system controller"""
        self.platform = platform.system()
        print(f"🖥️ System Controller initialized ({self.platform})")
        
        # Initialize volume control
        self.volume_control = None
        if VOLUME_CONTROL_AVAILABLE and self.platform == "Windows":
            try:
                # Method 1: Try standard approach
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
                print("   ✅ Volume control initialized")
            except AttributeError as e:
                # Method 2: Alternative for different pycaw versions
                print(f"   ⚠️ Standard volume control failed, trying alternative...")
                try:
                    import comtypes
                    from comtypes import CoInitialize, CoUninitialize
                    CoInitialize()
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
                    print("   ✅ Volume control initialized (alternative method)")
                except Exception as e2:
                    print(f"   ❌ Volume control unavailable: {e2}")
                    # Fallback: Use keyboard volume keys instead
                    print("   💡 Will use keyboard volume keys as fallback")
            except Exception as e:
                print(f"   ⚠️ Volume init error: {e}")
    
    # ========== VOLUME CONTROL ==========
    
    def volume_up(self, step=0.1):
        """
        Increase system volume
        
        Args:
            step (float): Volume increase amount (0.0 to 1.0)
        """
        if self.volume_control:
            try:
                current = self.volume_control.GetMasterVolumeLevelScalar()
                new_volume = min(1.0, current + step)
                self.volume_control.SetMasterVolumeLevelScalar(new_volume, None)
                print(f"🔊 Volume: {int(new_volume * 100)}%")
                return True
            except Exception as e:
                print(f"⚠️ Volume API failed, using keyboard shortcut...")
                # Fallback: Use keyboard volume up key
                if PYAUTOGUI_AVAILABLE:
                    try:
                        pyautogui.press('volumeup')
                        print("🔊 Volume increased (keyboard)")
                        return True
                    except:
                        pass
                print(f"❌ Volume up failed: {e}")
                return False
        else:
            # No API available, use keyboard
            if PYAUTOGUI_AVAILABLE:
                try:
                    pyautogui.press('volumeup')
                    print("🔊 Volume increased (keyboard)")
                    return True
                except Exception as e:
                    print(f"❌ Volume up failed: {e}")
                    return False
            print("⚠️ Volume control not available")
            return False
    
    def volume_down(self, step=0.1):
        """
        Decrease system volume
        
        Args:
            step (float): Volume decrease amount (0.0 to 1.0)
        """
        if self.volume_control:
            try:
                current = self.volume_control.GetMasterVolumeLevelScalar()
                new_volume = max(0.0, current - step)
                self.volume_control.SetMasterVolumeLevelScalar(new_volume, None)
                print(f"🔉 Volume: {int(new_volume * 100)}%")
                return True
            except Exception as e:
                print(f"⚠️ Volume API failed, using keyboard shortcut...")
                # Fallback: Use keyboard volume down key
                if PYAUTOGUI_AVAILABLE:
                    try:
                        pyautogui.press('volumedown')
                        print("🔉 Volume decreased (keyboard)")
                        return True
                    except:
                        pass
                print(f"❌ Volume down failed: {e}")
                return False
        else:
            # No API available, use keyboard
            if PYAUTOGUI_AVAILABLE:
                try:
                    pyautogui.press('volumedown')
                    print("🔉 Volume decreased (keyboard)")
                    return True
                except Exception as e:
                    print(f"❌ Volume down failed: {e}")
                    return False
            print("⚠️ Volume control not available")
            return False
    
    def volume_mute(self):
        """Toggle volume mute"""
        if self.volume_control:
            try:
                current_mute = self.volume_control.GetMute()
                self.volume_control.SetMute(not current_mute, None)
                status = "muted" if not current_mute else "unmuted"
                print(f"🔇 Volume {status}")
                return True
            except Exception as e:
                print(f"❌ Mute toggle failed: {e}")
                return False
        return False
    
    def get_volume(self):
        """
        Get current volume level
        
        Returns:
            float: Volume level (0.0 to 1.0) or None
        """
        if self.volume_control:
            try:
                return self.volume_control.GetMasterVolumeLevelScalar()
            except:
                return None
        return None
    
    # ========== BRIGHTNESS CONTROL ==========
    
    def brightness_up(self, step=10):
        """
        Increase screen brightness
        
        Args:
            step (int): Brightness increase (0-100)
        """
        if BRIGHTNESS_CONTROL_AVAILABLE:
            try:
                current = sbc.get_brightness()[0]
                new_brightness = min(100, current + step)
                sbc.set_brightness(new_brightness)
                print(f"☀️ Brightness: {new_brightness}%")
                return True
            except Exception as e:
                print(f"❌ Brightness up failed: {e}")
                return False
        else:
            print("⚠️ Brightness control not available")
            return False
    
    def brightness_down(self, step=10):
        """
        Decrease screen brightness
        
        Args:
            step (int): Brightness decrease (0-100)
        """
        if BRIGHTNESS_CONTROL_AVAILABLE:
            try:
                current = sbc.get_brightness()[0]
                new_brightness = max(0, current - step)
                sbc.set_brightness(new_brightness)
                print(f"🌙 Brightness: {new_brightness}%")
                return True
            except Exception as e:
                print(f"❌ Brightness down failed: {e}")
                return False
        else:
            print("⚠️ Brightness control not available")
            return False
    
    # ========== SCREENSHOT ==========
    
    def take_screenshot(self, filename=None):
        """
        Capture screenshot
        
        Args:
            filename (str, optional): Save path
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                if filename is None:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                
                screenshot = pyautogui.screenshot()
                screenshot.save(filename)
                print(f"📸 Screenshot saved: {filename}")
                return True
            except Exception as e:
                print(f"❌ Screenshot failed: {e}")
                return False
        else:
            print("⚠️ Screenshot not available (install pyautogui)")
            return False
    
    # ========== APPLICATION LAUNCHER ==========
    
    def open_application(self, app_name):
        """
        Open application
        
        Args:
            app_name (str): Application name
        """
        try:
            if self.platform == "Windows":
                app_map = {
                    'calculator': 'calc.exe',
                    'notepad': 'notepad.exe',
                    'paint': 'mspaint.exe',
                    'cmd': 'cmd.exe',
                    'explorer': 'explorer.exe'
                }
                
                cmd = app_map.get(app_name.lower(), app_name)
                subprocess.Popen(cmd, shell=True)
                print(f"🚀 Opened: {app_name}")
                return True
            else:
                # Linux/Mac support
                subprocess.Popen([app_name])
                return True
                
        except Exception as e:
            print(f"❌ Failed to open {app_name}: {e}")
            return False
    
    def open_calculator(self):
        """Open calculator"""
        return self.open_application('calculator')
    
    def open_notepad(self):
        """Open notepad"""
        return self.open_application('notepad')
    
    # ========== KEYBOARD SHORTCUTS ==========
    
    def minimize_all_windows(self):
        """Minimize all windows (Windows key + D)"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey('win', 'd')
                print("🪟 All windows minimized")
                return True
            except Exception as e:
                print(f"❌ Minimize failed: {e}")
                return False
        return False
    
    def alt_tab(self):
        """Switch windows (Alt+Tab)"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey('alt', 'tab')
                return True
            except:
                return False
        return False
    
    def task_manager(self):
        """Open task manager (Ctrl+Shift+Esc)"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey('ctrl', 'shift', 'esc')
                print("📊 Task manager opened")
                return True
            except:
                return False
        return False
    
    # ========== MEDIA CONTROL ==========
    
    def media_play_pause(self):
        """Toggle media play/pause"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press('playpause')
                print("⏯️ Media play/pause")
                return True
            except:
                return False
        return False
    
    def media_next(self):
        """Next track"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press('nexttrack')
                print("⏭️ Next track")
                return True
            except:
                return False
        return False
    
    def media_previous(self):
        """Previous track"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press('prevtrack')
                print("⏮️ Previous track")
                return True
            except:
                return False
        return False


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🖥️ TESTING SYSTEM CONTROLLER")
    print("=" * 50)
    
    controller = SystemController()
    
    print("\n🧪 Available controls:")
    print(f"   Volume control: {VOLUME_CONTROL_AVAILABLE}")
    print(f"   Brightness control: {BRIGHTNESS_CONTROL_AVAILABLE}")
    print(f"   PyAutoGUI: {PYAUTOGUI_AVAILABLE}")
    
    if VOLUME_CONTROL_AVAILABLE:
        current_vol = controller.get_volume()
        if current_vol:
            print(f"   Current volume: {int(current_vol * 100)}%")
    
    print("\n✅ System Controller tests completed!")
    print("\nNote: Full testing requires user interaction")
    print("Volume/brightness changes will be applied when called")