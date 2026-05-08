"""
GesturePilot - Final Version
Author: Your Name
Version: 1.0.0
Description: Complete gesture control system with GUI
"""

import cv2
import threading
import time
from camera_manager import CameraManager
from person_detector import PersonDetector
from hand_detector import HandDetector
from finger_analyzer import FingerAnalyzer
from gesture_recognizer import GestureRecognizer
from action_executor import ActionExecutor
from ui_manager import UIManager
from settings_panel import SettingsPanel
from history_manager import HistoryManager
from history_viewer import HistoryViewer
from autostart_manager import AutoStartManager
from config_manager import ConfigManager

class GesturePilot:
    """
    Complete GesturePilot Application - Final Version
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        """Initialize application"""
        print("=" * 60)
        print(f"🚀 GESTUREPILOT v{self.VERSION} - COMPLETE")
        print("=" * 60)
        
        # Configuration
        self.config = ConfigManager()
        
        # Core components
        self.camera = None
        self.person_detector = None
        self.hand_detector = None
        self.finger_analyzer = None
        self.gesture_recognizer = None
        self.action_executor = None
        
        # GUI components
        self.ui = None
        self.settings_panel = None
        self.history_viewer = None
        
        # Managers
        self.history = HistoryManager(
            max_size=self.config.get('advanced.max_history_size', 100)
        )
        self.autostart = AutoStartManager("GesturePilot")
        
        # State
        self.is_running = False
        self.is_paused = False
        self.show_skeleton = self.config.get('ui.show_skeleton', True)
        self.voice_enabled = self.config.get('ui.voice_feedback', True)
        
        # Threading
        self.processing_thread = None
        self.stop_event = threading.Event()
        
        print("\n📦 Initializing components...")
    
    def initialize(self):
        """Initialize all components"""
        try:
            # GUI
            print("\n🎨 Initializing GUI...")
            window_width = self.config.get('app.window_width', 1200)
            window_height = self.config.get('app.window_height', 850)
            
            self.ui = UIManager(
                title=f"GesturePilot v{self.VERSION}",
                width=window_width,
                height=window_height
            )
            
            # Set callbacks
            self.ui.on_settings_click = self.open_settings
            self.ui.on_history_click = self.open_history
            self.ui.on_pause_click = self.toggle_pause
            self.ui.on_stop_click = self.stop
            
            # Settings panel
            print("\n⚙️ Initializing Settings...")
            self.settings_panel = SettingsPanel(self.ui.get_root())
            self.settings_panel.on_settings_changed = self.apply_settings
            
            # History viewer
            print("\n📊 Initializing History Viewer...")
            self.history_viewer = HistoryViewer(self.ui.get_root(), self.history)
            
            # Detection components
            print("\n1️⃣ Camera...")
            cam_width = self.config.get('camera.resolution_width', 1280)
            cam_height = self.config.get('camera.resolution_height', 720)
            cam_fps = self.config.get('camera.fps', 30)
            
            self.camera = CameraManager(width=cam_width, height=cam_height, fps=cam_fps)
            if not self.camera.initialize_camera():
                return False
            
            print("\n2️⃣ Person Detector...")
            self.person_detector = PersonDetector()
            
            print("\n3️⃣ Hand Detector...")
            self.hand_detector = HandDetector(max_num_hands=2)
            
            print("\n4️⃣ Finger Analyzer...")
            self.finger_analyzer = FingerAnalyzer()
            
            print("\n5️⃣ Gesture Recognizer...")
            self.gesture_recognizer = GestureRecognizer()
            
            print("\n6️⃣ Action Executor...")
            self.action_executor = ActionExecutor(voice_enabled=self.voice_enabled)
            
            # Update UI with initial state
            self.ui.update_voice_status(self.voice_enabled)
            
            print("\n✅ All systems ready!")
            
            # Check first run
            if self.config.get('app.first_run', True):
                print("\n👋 Welcome to GesturePilot!")
                self.config.set('app.first_run', False)
                self.config.save_config()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_frame(self):
        """Process frames in background thread"""
        print("🎬 Starting frame processing...")
        
        while not self.stop_event.is_set():
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            try:
                # Get frame
                success, frame_rgb, fps = self.camera.get_frame()
                
                if not success:
                    continue
                
                # Update FPS
                self.ui.update_fps(fps)
                
                # Person validation
                is_valid, msg, person_data = \
                    self.person_detector.validate_single_person(frame_rgb)
                
                self.ui.update_person_status(is_valid, msg)
                
                # Convert for display
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                
                hands_data = []
                
                if is_valid:
                    # Hand detection
                    hand_results = self.hand_detector.detect_hands(frame_rgb)
                    hands_data = self.hand_detector.get_hand_landmarks(hand_results)
                    
                    self.ui.update_hands_count(len(hands_data))
                    
                    # Draw skeleton
                    if self.show_skeleton and hand_results:
                        frame_bgr = self.hand_detector.draw_hand_skeleton(
                            frame_bgr, hand_results
                        )
                    
                    # Process each hand
                    for hand_data in hands_data:
                        finger_states = self.finger_analyzer.analyze_fingers(
                            hand_data['landmarks'],
                            hand_data['hand_type']
                        )
                        
                        if finger_states:
                            result = self.gesture_recognizer.recognize_gesture(
                                finger_states
                            )
                            
                            if result['recognized']:
                                gesture = result['gesture']
                                
                                # Update UI
                                self.ui.update_gesture_info(
                                    gesture['name'],
                                    gesture['action'],
                                    result['confidence']
                                )
                                
                                # Execute action
                                success = self.action_executor.execute(gesture['action'])
                                
                                # Record in history
                                self.history.add_action(
                                    gesture['name'],
                                    gesture['action'],
                                    hand_data['hand_type'],
                                    result['confidence'],
                                    'success' if success else 'failed'
                                )
                
                else:
                    self.ui.update_hands_count(0)
                
                # Update camera display
                self.ui.update_camera_frame(frame_bgr)
                
            except Exception as e:
                print(f"⚠️ Processing error: {e}")
                time.sleep(0.1)
        
        print("🛑 Frame processing stopped")
    
    def open_settings(self):
        """Open settings panel"""
        print("⚙️ Opening settings...")
        self.settings_panel.show()
    
    def open_history(self):
        """Open history viewer"""
        print("📊 Opening history...")
        self.history_viewer.show()
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        status = "PAUSED" if self.is_paused else "RESUMED"
        print(f"⏸️  {status}")
        return self.is_paused
    
    def apply_settings(self, settings):
        """Apply settings changes"""
        print("💾 Applying settings...")
        
        # Update voice
        if 'voice_feedback' in settings:
            self.voice_enabled = settings['voice_feedback']
            self.action_executor.set_voice_enabled(self.voice_enabled)
            self.ui.update_voice_status(self.voice_enabled)
            self.config.set('ui.voice_feedback', self.voice_enabled)
        
        # Update skeleton
        if 'show_skeleton' in settings:
            self.show_skeleton = settings['show_skeleton']
            self.config.set('ui.show_skeleton', self.show_skeleton)
        
        # Update FPS display
        if 'show_fps' in settings:
            self.config.set('ui.show_fps', settings['show_fps'])
        
        # Update autostart
        if 'autostart' in settings:
            if settings['autostart']:
                self.autostart.enable()
            else:
                self.autostart.disable()
            self.config.set('autostart.enabled', settings['autostart'])
        
        # Update confidence threshold
        if 'confidence_threshold' in settings:
            self.config.set('detection.confidence_threshold', settings['confidence_threshold'])
        
        # Update cooldown
        if 'cooldown_duration' in settings:
            self.config.set('detection.cooldown_duration', settings['cooldown_duration'])
        
        # Save config
        self.config.save_config()
        
        print("✅ Settings applied and saved!")
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            print("\n❌ Initialization failed. Exiting...")
            return
        
        print("\n" + "=" * 60)
        print("🎬 GESTUREPILOT READY!")
        print("=" * 60)
        print(f"\n✨ Version {self.VERSION}")
        print("🎨 Dark mode GUI active")
        print("🎯 Gesture recognition ready")
        print("📊 History tracking enabled")
        print("⚙️  Click 'Settings' to customize")
        
        # Check autostart status
        if self.autostart.is_enabled():
            print("🚀 Auto-start: Enabled")
        
        print("\n" + "=" * 60 + "\n")
        
        # Start processing thread
        self.is_running = True
        self.processing_thread = threading.Thread(target=self.process_frame)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        try:
            # Start UI (blocks until window closed)
            self.ui.start()
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def stop(self):
        """Stop application"""
        print("\n🛑 Stopping GesturePilot...")
        self.stop_event.set()
        self.is_running = False
        
        # Save history before exit
        self.history.save_history()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n" + "=" * 60)
        print("🧹 SHUTTING DOWN")
        print("=" * 60)
        
        self.stop_event.set()
        
        # Wait for processing thread
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
        
        # Release resources
        if self.hand_detector:
            self.hand_detector.release()
        
        if self.person_detector:
            self.person_detector.release()
        
        if self.camera:
            self.camera.release_camera()
        
        # Save final state
        self.history.save_history()
        self.config.save_config()
        
        print("\n✅ Cleanup complete!")
        print("\n" + "=" * 60)
        print(f"👋 GESTUREPILOT v{self.VERSION} - GOODBYE!")
        print("=" * 60)


def main():
    """Entry point"""
    app = GesturePilot()
    app.run()


if __name__ == "__main__":
    main()