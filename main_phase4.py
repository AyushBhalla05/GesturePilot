"""
GesturePilot - Phase 4: Complete GUI Application
Author: Your Name
Description: Full application with dark mode GUI
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

class GesturePilotPhase4:
    """
    Complete GesturePilot with dark mode GUI
    """
    
    def __init__(self):
        """Initialize application"""
        print("=" * 60)
        print("🚀 GESTUREPILOT - PHASE 4: GUI APPLICATION")
        print("=" * 60)
        
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
        
        # State
        self.is_running = False
        self.is_paused = False
        self.show_skeleton = True
        self.voice_enabled = True
        
        # Threading
        self.processing_thread = None
        self.stop_event = threading.Event()
        
        print("\n📦 Initializing...")
    
    def initialize(self):
        """Initialize all components"""
        try:
            print("\n🎨 Initializing GUI...")
            self.ui = UIManager(title="GesturePilot - Phase 4", width=1200, height=850)
            
            # Set callbacks
            self.ui.on_settings_click = self.open_settings
            self.ui.on_pause_click = self.toggle_pause
            self.ui.on_stop_click = self.stop
            
            print("\n⚙️ Initializing Settings Panel...")
            self.settings_panel = SettingsPanel(self.ui.get_root())
            self.settings_panel.on_settings_changed = self.apply_settings
            
            print("\n1️⃣ Camera...")
            self.camera = CameraManager(width=1280, height=720, fps=30)
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
            
            print("\n✅ All systems ready!")
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
                
                # Update FPS in UI
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
                                self.action_executor.execute(gesture['action'])
                
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
        
        # Update skeleton
        if 'show_skeleton' in settings:
            self.show_skeleton = settings['show_skeleton']
        
        print("✅ Settings applied!")
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            print("\n❌ Initialization failed. Exiting...")
            return
        
        print("\n" + "=" * 60)
        print("🎬 GESTUREPILOT STARTING!")
        print("=" * 60)
        print("\n✨ Dark mode GUI loaded")
        print("🎯 Ready for gesture recognition")
        print("⚙️  Click 'Settings' to customize")
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
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n" + "=" * 60)
        print("🧹 SHUTTING DOWN")
        print("=" * 60)
        
        self.stop_event.set()
        
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
        
        if self.hand_detector:
            self.hand_detector.release()
        
        if self.person_detector:
            self.person_detector.release()
        
        if self.camera:
            self.camera.release_camera()
        
        print("\n✅ Cleanup complete!")
        print("\n" + "=" * 60)
        print("👋 GESTUREPILOT - GOODBYE!")
        print("=" * 60)


def main():
    """Entry point"""
    app = GesturePilotPhase4()
    app.run()


if __name__ == "__main__":
    main()