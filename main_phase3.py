"""
GesturePilot - Phase 3: Complete Application with Action Execution
Author: Your Name
Description: Full gesture control system with actions and voice feedback
"""

import cv2
import time
from camera_manager import CameraManager
from person_detector import PersonDetector
from hand_detector import HandDetector
from finger_analyzer import FingerAnalyzer
from gesture_recognizer import GestureRecognizer
from action_executor import ActionExecutor

class GesturePilotPhase3:
    """
    Complete GesturePilot application with action execution
    """
    
    def __init__(self):
        """Initialize all components"""
        print("=" * 60)
        print("🚀 GESTUREPILOT - PHASE 3: COMPLETE APPLICATION")
        print("=" * 60)
        
        # All components
        self.camera = None
        self.person_detector = None
        self.hand_detector = None
        self.finger_analyzer = None
        self.gesture_recognizer = None
        self.action_executor = None
        
        # State
        self.is_running = False
        self.show_hand_skeleton = True
        self.voice_enabled = True
        
        # Confirmation display
        self.last_action = None
        self.last_action_time = 0
        self.action_display_duration = 1.0
        
        print("\n📦 Initializing components...")
    
    def initialize(self):
        """Initialize all components"""
        try:
            # Phase 1: Detection
            print("\n1️⃣ Camera...")
            self.camera = CameraManager(width=1280, height=720, fps=30)
            if not self.camera.initialize_camera():
                return False
            
            print("\n2️⃣ Person Detector...")
            self.person_detector = PersonDetector()
            
            print("\n3️⃣ Hand Detector...")
            self.hand_detector = HandDetector(max_num_hands=2)
            
            # Phase 2: Recognition
            print("\n4️⃣ Finger Analyzer...")
            self.finger_analyzer = FingerAnalyzer()
            
            print("\n5️⃣ Gesture Recognizer...")
            self.gesture_recognizer = GestureRecognizer()
            
            # Phase 3: Action
            print("\n6️⃣ Action Executor...")
            self.action_executor = ActionExecutor(voice_enabled=self.voice_enabled)
            
            print("\n✅ All systems ready!")
            return True
            
        except Exception as e:
            print(f"\n❌ Initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_frame(self, frame_rgb, frame_bgr, fps):
        """Process frame and execute actions"""
        
        # Step 1: Person validation
        is_valid_person, person_msg, person_data = \
            self.person_detector.validate_single_person(frame_rgb)
        
        hands_data = []
        recognized_gestures = []
        
        if is_valid_person:
            # Step 2: Hand detection
            hand_results = self.hand_detector.detect_hands(frame_rgb)
            hands_data = self.hand_detector.get_hand_landmarks(hand_results)
            
            # Step 3: Process each hand
            for hand_data in hands_data:
                # Analyze fingers
                finger_states = self.finger_analyzer.analyze_fingers(
                    hand_data['landmarks'],
                    hand_data['hand_type']
                )
                
                if finger_states:
                    # Recognize gesture
                    result = self.gesture_recognizer.recognize_gesture(finger_states)
                    
                    result['hand_data'] = hand_data
                    result['finger_states'] = finger_states
                    recognized_gestures.append(result)
                    
                    # Execute action if confirmed
                    if result['recognized']:
                        gesture = result['gesture']
                        action_name = gesture['action']
                        
                        # Execute!
                        success = self.action_executor.execute(action_name)
                        
                        if success:
                            self.last_action = gesture
                            self.last_action_time = time.time()
            
            # Draw hand skeleton
            if self.show_hand_skeleton and hand_results:
                frame_bgr = self.hand_detector.draw_hand_skeleton(frame_bgr, hand_results)
        
        # Draw UI
        frame_bgr = self._draw_status(frame_bgr, person_msg, is_valid_person)
        frame_bgr = self._draw_gesture_info(frame_bgr, recognized_gestures)
        frame_bgr = self._draw_action_flash(frame_bgr)
        frame_bgr = self._draw_ui(frame_bgr, fps, is_valid_person, 
                                   len(hands_data), len(recognized_gestures))
        
        return frame_bgr
    
    def _draw_status(self, frame_bgr, message, is_valid):
        """Draw status message"""
        h, w = frame_bgr.shape[:2]
        color = (0, 255, 0) if is_valid else (0, 0, 255)
        
        # Background
        cv2.rectangle(frame_bgr, (w//4, 100), (3*w//4, 150), (0, 0, 0), -1)
        cv2.rectangle(frame_bgr, (w//4, 100), (3*w//4, 150), color, 2)
        
        # Text
        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(frame_bgr, message, (text_x, 135),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        return frame_bgr
    
    def _draw_gesture_info(self, frame_bgr, gestures):
        """Draw gesture information"""
        h, w = frame_bgr.shape[:2]
        y = 200
        
        for result in gestures:
            hand = result.get('hand_data', {}).get('hand_type', 'Unknown')
            pattern = result.get('finger_states', {}).get('pattern', [0,0,0,0,0])
            
            color = (0, 0, 255) if hand == 'Right' else (255, 0, 0)
            
            # Hand + pattern
            text = f"{hand}: {pattern}"
            cv2.putText(frame_bgr, text, (20, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y += 30
            
            # Status
            if result['recognized']:
                gesture = result['gesture']
                conf = result['confidence']
                text = f"  ✓ {gesture['icon']} {gesture['name']} ({conf:.0f}%)"
                cv2.putText(frame_bgr, text, (20, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            elif result['cooldown_active']:
                remaining = self.gesture_recognizer.get_cooldown_remaining(hand)
                text = f"  ⏱ Cooldown: {remaining:.1f}s"
                cv2.putText(frame_bgr, text, (20, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            elif result['status'] == 'low_confidence':
                conf = result['confidence']
                text = f"  ? Detecting... ({conf:.0f}%)"
                cv2.putText(frame_bgr, text, (20, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            y += 40
        
        return frame_bgr
    
    def _draw_action_flash(self, frame_bgr):
        """Draw action execution flash"""
        if not self.last_action:
            return frame_bgr
        
        elapsed = time.time() - self.last_action_time
        
        if elapsed < self.action_display_duration:
            h, w = frame_bgr.shape[:2]
            alpha = 1.0 - (elapsed / self.action_display_duration)
            
            # Green flash overlay
            overlay = frame_bgr.copy()
            cv2.rectangle(overlay, (w//4, h//3), (3*w//4, 2*h//3),
                         (0, 255, 0), -1)
            cv2.addWeighted(overlay, alpha * 0.3, frame_bgr, 1, 0, frame_bgr)
            
            # Icon
            icon = self.last_action.get('icon', '✓')
            text_size = cv2.getTextSize(icon, cv2.FONT_HERSHEY_SIMPLEX, 3.0, 4)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, icon, (text_x, h//2 - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 255, 0), 4)
            
            # Name
            name = self.last_action['name']
            text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, name, (text_x, h//2 + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            
            # Action
            action = self.last_action['action'].replace('_', ' ').upper()
            text_size = cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, action, (text_x, h//2 + 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        return frame_bgr
    
    def _draw_ui(self, frame_bgr, fps, person_valid, hand_count, gesture_count):
        """Draw UI elements"""
        h, w = frame_bgr.shape[:2]
        
        # Top bar
        overlay = frame_bgr.copy()
        cv2.rectangle(overlay, (0, 0), (w, 90), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame_bgr, 0.3, 0, frame_bgr)
        
        # FPS
        fps_color = (0, 255, 0) if fps > 25 else (0, 165, 255)
        cv2.putText(frame_bgr, f"FPS: {int(fps)}", (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, fps_color, 2)
        
        # Person
        person_color = (0, 255, 0) if person_valid else (0, 0, 255)
        person_icon = "✓" if person_valid else "✗"
        cv2.putText(frame_bgr, f"Person: {person_icon}", (20, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, person_color, 2)
        
        # Hands
        hand_color = (0, 255, 0) if hand_count > 0 else (150, 150, 150)
        cv2.putText(frame_bgr, f"Hands: {hand_count}", (w//2 - 80, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, hand_color, 2)
        
        # Gestures
        if gesture_count > 0:
            cv2.putText(frame_bgr, f"🎯 Active: {gesture_count}", (w//2 - 100, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Voice status
        voice_status = "🔊 ON" if self.voice_enabled else "🔇 OFF"
        cv2.putText(frame_bgr, voice_status, (w - 150, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Controls
        controls = [
            "CONTROLS:",
            "'Q' - Quit  |  'V' - Voice  |  'H' - Skeleton",
            "'R' - Reload  |  'SPACE' - Pause"
        ]
        
        y = h - 100
        for control in controls:
            cv2.putText(frame_bgr, control, (20, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            y += 30
        
        # Status
        cv2.putText(frame_bgr, "PHASE 3 - ACTIVE", (w - 260, h - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return frame_bgr
    
    def run(self):
        """Main loop"""
        if not self.initialize():
            print("\n❌ Failed to initialize. Exiting...")
            return
        
        print("\n" + "=" * 60)
        print("🎬 GESTUREPILOT READY!")
        print("=" * 60)
        print("\n⌨️  CONTROLS:")
        print("   Q       - Quit")
        print("   V       - Toggle Voice Feedback")
        print("   H       - Toggle Hand Skeleton")
        print("   R       - Reload Gestures")
        print("   SPACE   - Pause/Resume")
        print("\n🎯 GESTURES:")
        print("   Right hand gestures execute actions!")
        print("   Hold gesture for 0.5s to trigger")
        print("   2s cooldown between actions")
        print("\n" + "=" * 60 + "\n")
        
        self.is_running = True
        frame_count = 0
        paused = False
        
        try:
            while True:
                success, frame_rgb, fps = self.camera.get_frame()
                
                if not success:
                    continue
                
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                
                if not paused:
                    frame_bgr = self.process_frame(frame_rgb, frame_bgr, fps)
                else:
                    h, w = frame_bgr.shape[:2]
                    cv2.putText(frame_bgr, "PAUSED", (w//2 - 120, h//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 165, 255), 4)
                
                cv2.imshow("GesturePilot - Complete", frame_bgr)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:
                    break
                elif key == ord('v'):
                    self.voice_enabled = not self.voice_enabled
                    self.action_executor.set_voice_enabled(self.voice_enabled)
                    status = "ON" if self.voice_enabled else "OFF"
                    print(f"🔊 Voice: {status}")
                elif key == ord('h'):
                    self.show_hand_skeleton = not self.show_hand_skeleton
                    print(f"🤚 Skeleton: {'ON' if self.show_hand_skeleton else 'OFF'}")
                elif key == ord('r'):
                    self.gesture_recognizer.reload_library()
                elif key == ord(' '):
                    paused = not paused
                    print(f"⏸️  {'PAUSED' if paused else 'RESUMED'}")
                
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"📊 {frame_count} frames | FPS: {int(fps)}")
        
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup"""
        print("\n" + "=" * 60)
        print("🧹 SHUTTING DOWN")
        print("=" * 60)
        
        if self.hand_detector:
            self.hand_detector.release()
        if self.person_detector:
            self.person_detector.release()
        if self.camera:
            self.camera.release_camera()
        
        cv2.destroyAllWindows()
        
        print("\n✅ Shutdown complete!")
        print("\n" + "=" * 60)
        print("👋 GESTUREPILOT - GOODBYE!")
        print("=" * 60)


def main():
    """Entry point"""
    app = GesturePilotPhase3()
    app.run()


if __name__ == "__main__":
    main()