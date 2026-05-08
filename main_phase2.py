"""
GesturePilot - Phase 2: Complete Integration with Gesture Recognition
Author: Your Name
Description: Integrates all Phase 1 + Phase 2 components
"""

import cv2
import time
from camera_manager import CameraManager
from person_detector import PersonDetector
from hand_detector import HandDetector
from finger_analyzer import FingerAnalyzer
from gesture_recognizer import GestureRecognizer

class GesturePilotPhase2:
    """
    Main application class for Phase 2
    Adds gesture recognition to Phase 1 foundation
    """
    
    def __init__(self):
        """Initialize all components"""
        print("=" * 60)
        print("🚀 GESTUREPILOT - PHASE 2: GESTURE RECOGNITION")
        print("=" * 60)
        
        # Phase 1 components
        self.camera = None
        self.person_detector = None
        self.hand_detector = None
        
        # Phase 2 components
        self.finger_analyzer = None
        self.gesture_recognizer = None
        
        # State variables
        self.is_running = False
        self.show_hand_skeleton = True
        self.show_debug_info = True  # Toggle with 'd' key
        
        # Gesture confirmation
        self.last_confirmed_gesture = None
        self.confirmation_time = 0
        self.confirmation_duration = 0.5  # seconds
        
        print("\n📦 Initializing components...")
    
    def initialize(self):
        """
        Initialize all components
        
        Returns:
            bool: True if successful
        """
        try:
            # Phase 1 components
            print("\n1️⃣ Initializing Camera...")
            self.camera = CameraManager(width=1280, height=720, fps=30)
            if not self.camera.initialize_camera():
                return False
            
            print("\n2️⃣ Initializing Person Detector...")
            self.person_detector = PersonDetector()
            
            print("\n3️⃣ Initializing Hand Detector...")
            self.hand_detector = HandDetector(max_num_hands=2)
            
            # Phase 2 components
            print("\n4️⃣ Initializing Finger Analyzer...")
            self.finger_analyzer = FingerAnalyzer()
            
            print("\n5️⃣ Initializing Gesture Recognizer...")
            self.gesture_recognizer = GestureRecognizer()
            
            print("\n✅ All components initialized successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Initialization error: {e}")
            return False
    
    def process_frame(self, frame_rgb, frame_bgr, fps):
        """
        Process frame through complete pipeline
        
        Args:
            frame_rgb: Frame in RGB
            frame_bgr: Frame in BGR
            fps: Current FPS
            
        Returns:
            numpy.ndarray: Processed frame
        """
        # Step 1: Validate person
        is_valid_person, person_msg, person_data = \
            self.person_detector.validate_single_person(frame_rgb)
        
        # Step 2: Detect hands
        hands_data = []
        hand_results = None
        recognized_gestures = []
        
        if is_valid_person:
            hand_results = self.hand_detector.detect_hands(frame_rgb)
            hands_data = self.hand_detector.get_hand_landmarks(hand_results)
            
            # Step 3: Analyze fingers for each hand
            for hand_data in hands_data:
                # Get finger states
                finger_states = self.finger_analyzer.analyze_fingers(
                    hand_data['landmarks'],
                    hand_data['hand_type']
                )
                
                if finger_states:
                    # Step 4: Recognize gesture
                    recognition_result = self.gesture_recognizer.recognize_gesture(
                        finger_states
                    )
                    
                    # Store result with hand data
                    recognition_result['hand_data'] = hand_data
                    recognition_result['finger_states'] = finger_states
                    recognized_gestures.append(recognition_result)
                    
                    # Check for confirmed gesture
                    if recognition_result['recognized']:
                        self.last_confirmed_gesture = recognition_result['gesture']
                        self.confirmation_time = time.time()
        
        # Draw visualizations
        if self.show_hand_skeleton and hand_results:
            frame_bgr = self.hand_detector.draw_hand_skeleton(frame_bgr, hand_results)
        
        # Draw status
        frame_bgr = self.person_detector.draw_status_message(
            frame_bgr, person_msg, is_valid_person
        )
        
        # Draw gesture info
        frame_bgr = self._draw_gesture_info(frame_bgr, recognized_gestures)
        
        # Draw confirmation flash
        frame_bgr = self._draw_confirmation_flash(frame_bgr)
        
        # Draw UI
        frame_bgr = self._draw_ui(frame_bgr, fps, is_valid_person, 
                                   hands_data, recognized_gestures)
        
        return frame_bgr
    
    def _draw_gesture_info(self, frame_bgr, recognized_gestures):
        """Draw gesture recognition information"""
        h, w = frame_bgr.shape[:2]
        y_offset = 150
        
        for result in recognized_gestures:
            hand_type = result.get('hand_data', {}).get('hand_type', 'Unknown')
            finger_states = result.get('finger_states', {})
            pattern = finger_states.get('pattern', [0, 0, 0, 0, 0])
            
            # Color based on hand
            color = (0, 0, 255) if hand_type == 'Right' else (255, 0, 0)
            
            # Draw hand type and pattern
            text = f"{hand_type}: {pattern}"
            cv2.putText(frame_bgr, text, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_offset += 30
            
            # Draw recognition status
            status = result['status']
            confidence = result['confidence']
            
            if result['recognized']:
                gesture = result['gesture']
                text = f"  ✓ {gesture['icon']} {gesture['name']} ({confidence:.0f}%)"
                status_color = (0, 255, 0)
            elif result['cooldown_active']:
                remaining = self.gesture_recognizer.get_cooldown_remaining(hand_type)
                text = f"  ⏱ Cooldown: {remaining:.1f}s"
                status_color = (0, 165, 255)
            elif status == 'low_confidence':
                text = f"  ? Detecting... ({confidence:.0f}%)"
                status_color = (0, 255, 255)
            else:
                text = f"  • Pattern: {self.finger_analyzer.pattern_to_string(pattern)}"
                status_color = (200, 200, 200)
            
            cv2.putText(frame_bgr, text, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
            y_offset += 40
        
        return frame_bgr
    
    def _draw_confirmation_flash(self, frame_bgr):
        """Draw gesture confirmation flash"""
        if not self.last_confirmed_gesture:
            return frame_bgr
        
        elapsed = time.time() - self.confirmation_time
        
        if elapsed < self.confirmation_duration:
            h, w = frame_bgr.shape[:2]
            
            # Create flash effect
            alpha = 1.0 - (elapsed / self.confirmation_duration)
            
            # Draw semi-transparent overlay
            overlay = frame_bgr.copy()
            cv2.rectangle(overlay, (w//4, h//3), (3*w//4, 2*h//3),
                         (0, 255, 0), -1)
            cv2.addWeighted(overlay, alpha * 0.3, frame_bgr, 1 - alpha * 0.3, 0, frame_bgr)
            
            # Draw gesture info
            gesture = self.last_confirmed_gesture
            icon = gesture.get('icon', '✓')
            name = gesture.get('name', 'Gesture')
            action = gesture.get('action', '')
            
            # Large icon
            text = f"{icon}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 3.0, 4)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, text, (text_x, h//2 - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 255, 0), 4)
            
            # Gesture name
            text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, name, (text_x, h//2 + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            
            # Action name
            text_size = cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame_bgr, f"Action: {action}", (text_x, h//2 + 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        return frame_bgr
    
    def _draw_ui(self, frame_bgr, fps, is_valid_person, hands_data, recognized_gestures):
        """Draw UI elements"""
        h, w = frame_bgr.shape[:2]
        
        # Top status bar
        overlay = frame_bgr.copy()
        cv2.rectangle(overlay, (0, 0), (w, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame_bgr, 0.4, 0, frame_bgr)
        
        # FPS
        fps_color = (0, 255, 0) if fps > 25 else (0, 165, 255)
        cv2.putText(frame_bgr, f"FPS: {int(fps)}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2)
        
        # Person status
        person_color = (0, 255, 0) if is_valid_person else (0, 0, 255)
        person_icon = "✓" if is_valid_person else "✗"
        cv2.putText(frame_bgr, f"Person: {person_icon}", (w//2 - 100, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, person_color, 2)
        
        # Hands count
        hand_color = (0, 255, 0) if hands_data else (150, 150, 150)
        cv2.putText(frame_bgr, f"Hands: {len(hands_data)}", (w - 220, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, hand_color, 2)
        
        # Recognized gestures count
        recognized_count = sum(1 for r in recognized_gestures if r['recognized'])
        if recognized_count > 0:
            cv2.putText(frame_bgr, f"🎯 Gestures: {recognized_count}", (w - 220, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Controls (bottom)
        controls = [
            "PHASE 2 CONTROLS:",
            "'Q' - Quit",
            "'H' - Toggle Skeleton",
            "'D' - Toggle Debug",
            "'R' - Reload Gestures",
            "'SPACE' - Pause"
        ]
        
        y_start = h - 210
        for i, control in enumerate(controls):
            cv2.putText(frame_bgr, control, (20, y_start + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Status
        cv2.putText(frame_bgr, "PHASE 2 ACTIVE", (w - 240, h - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return frame_bgr
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            print("\n❌ Failed to initialize. Exiting...")
            return
        
        print("\n" + "=" * 60)
        print("🎬 STARTING GESTURE RECOGNITION")
        print("=" * 60)
        print("\n⌨️  CONTROLS:")
        print("   Q     - Quit")
        print("   H     - Toggle Hand Skeleton")
        print("   D     - Toggle Debug Info")
        print("   R     - Reload Gesture Library")
        print("   SPACE - Pause/Resume")
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
                    cv2.putText(frame_bgr, "PAUSED", (w//2 - 100, h//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 165, 255), 4)
                
                cv2.imshow("GesturePilot - Phase 2", frame_bgr)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:
                    break
                elif key == ord('h'):
                    self.show_hand_skeleton = not self.show_hand_skeleton
                    print(f"🤚 Hand skeleton: {'ON' if self.show_hand_skeleton else 'OFF'}")
                elif key == ord('d'):
                    self.show_debug_info = not self.show_debug_info
                    print(f"🐛 Debug info: {'ON' if self.show_debug_info else 'OFF'}")
                elif key == ord('r'):
                    self.gesture_recognizer.reload_library()
                elif key == ord(' '):
                    paused = not paused
                    print(f"⏸️  {'PAUSED' if paused else 'RESUMED'}")
                
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"📊 Processed {frame_count} frames | FPS: {int(fps)}")
        
        except KeyboardInterrupt:
            print("\n⚠️ Keyboard interrupt...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n" + "=" * 60)
        print("🧹 CLEANING UP")
        print("=" * 60)
        
        if self.hand_detector:
            self.hand_detector.release()
        if self.person_detector:
            self.person_detector.release()
        if self.camera:
            self.camera.release_camera()
        
        cv2.destroyAllWindows()
        
        print("\n✅ Cleanup completed!")
        print("\n" + "=" * 60)
        print("👋 GESTUREPILOT PHASE 2 - STOPPED")
        print("=" * 60)


def main():
    """Entry point"""
    app = GesturePilotPhase2()
    app.run()


if __name__ == "__main__":
    main()