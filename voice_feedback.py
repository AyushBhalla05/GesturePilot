"""
GesturePilot - Phase 3: Voice Feedback System
Author: Your Name
Description: Text-to-speech feedback for gesture actions
"""

import os
import threading
from pathlib import Path

try:
    from gtts import gTTS
    import pygame
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Voice feedback libraries not installed")
    print("   Install: pip install gTTS pygame")

class VoiceFeedback:
    """
    Provides voice feedback for actions using Google Text-to-Speech
    """
    
    def __init__(self, enabled=True, cache_dir='cache/audio'):
        """
        Initialize voice feedback system
        
        Args:
            enabled (bool): Enable/disable voice feedback
            cache_dir (str): Directory for audio cache
        """
        self.enabled = enabled and VOICE_AVAILABLE
        self.cache_dir = Path(cache_dir)
        self.cache = {}
        
        if not VOICE_AVAILABLE:
            self.enabled = False
            return
        
        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            print("🔊 Voice Feedback initialized")
            print(f"   Cache directory: {self.cache_dir}")
        except Exception as e:
            print(f"❌ Failed to initialize audio: {e}")
            self.enabled = False
    
    def speak(self, text, async_mode=True):
        """
        Speak the given text
        
        Args:
            text (str): Text to speak
            async_mode (bool): Play audio asynchronously
        """
        if not self.enabled:
            return
        
        if async_mode:
            # Play in background thread
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text):
        """
        Synchronous speech (internal use)
        
        Args:
            text (str): Text to speak
        """
        try:
            # Check cache
            audio_file = self._get_cached_audio(text)
            
            if not audio_file.exists():
                # Generate audio
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(str(audio_file))
            
            # Play audio
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except Exception as e:
            print(f"⚠️ Voice feedback error: {e}")
    
    def _get_cached_audio(self, text):
        """
        Get cached audio file path for text
        
        Args:
            text (str): Text to cache
            
        Returns:
            Path: Audio file path
        """
        # Create safe filename from text
        safe_name = "".join(c if c.isalnum() else "_" for c in text)
        safe_name = safe_name[:50]  # Limit length
        
        filename = f"{safe_name}.mp3"
        return self.cache_dir / filename
    
    def announce_gesture(self, gesture_name, action_name=None):
        """
        Announce gesture detection
        
        Args:
            gesture_name (str): Name of detected gesture
            action_name (str, optional): Action being performed
        """
        if action_name:
            text = action_name.replace('_', ' ')
        else:
            text = gesture_name
        
        self.speak(text)
    
    def announce_action(self, action_name):
        """
        Announce action execution
        
        Args:
            action_name (str): Action name
        """
        # Convert action name to readable text
        text = self._action_to_speech(action_name)
        self.speak(text)
    
    def _action_to_speech(self, action_name):
        """
        Convert action name to speech text
        
        Args:
            action_name (str): Action identifier
            
        Returns:
            str: Speech text
        """
        speech_map = {
            'open_youtube': 'Opening YouTube',
            'music_play_pause': 'Music toggled',
            'music_next': 'Next track',
            'music_previous': 'Previous track',
            'volume_up': 'Volume up',
            'volume_down': 'Volume down',
            'brightness_up': 'Brightness up',
            'brightness_down': 'Brightness down',
            'take_screenshot': 'Screenshot captured',
            'open_calculator': 'Opening calculator',
            'open_notepad': 'Opening notepad',
            'browser_new_tab': 'New tab',
            'browser_close_tab': 'Tab closed',
            'minimize_all': 'Windows minimized',
            'stop_action': 'Stopped'
        }
        
        return speech_map.get(action_name, action_name.replace('_', ' '))
    
    def announce_error(self, error_message):
        """
        Announce error message
        
        Args:
            error_message (str): Error description
        """
        self.speak(f"Error: {error_message}")
    
    def announce_status(self, status):
        """
        Announce system status
        
        Args:
            status (str): Status message
        """
        self.speak(status)
    
    def clear_cache(self):
        """
        Clear audio cache
        """
        try:
            for file in self.cache_dir.glob('*.mp3'):
                file.unlink()
            print("🗑️ Audio cache cleared")
        except Exception as e:
            print(f"⚠️ Could not clear cache: {e}")
    
    def set_enabled(self, enabled):
        """
        Enable/disable voice feedback
        
        Args:
            enabled (bool): Enable state
        """
        if VOICE_AVAILABLE:
            self.enabled = enabled
            status = "enabled" if enabled else "disabled"
            print(f"🔊 Voice feedback {status}")
    
    def is_enabled(self):
        """
        Check if voice feedback is enabled
        
        Returns:
            bool: Enabled state
        """
        return self.enabled
    
    def test_voice(self):
        """
        Test voice feedback
        """
        if not self.enabled:
            print("❌ Voice feedback is disabled")
            return
        
        print("🔊 Testing voice feedback...")
        self.speak("Gesture Pilot voice feedback is working", async_mode=False)
        print("✅ Voice test completed")


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🔊 TESTING VOICE FEEDBACK")
    print("=" * 50)
    
    # Create voice feedback
    voice = VoiceFeedback(enabled=True)
    
    if voice.is_enabled():
        print("\n🧪 Test 1: Basic speech")
        voice.test_voice()
        
        print("\n🧪 Test 2: Action announcements")
        actions = [
            'open_youtube',
            'volume_up',
            'take_screenshot'
        ]
        
        for action in actions:
            print(f"   Announcing: {action}")
            voice.announce_action(action)
            import time
            time.sleep(2)  # Wait between announcements
        
        print("\n✅ Voice feedback tests completed!")
    else:
        print("\n❌ Voice feedback not available")
        print("   Install: pip install gTTS pygame")