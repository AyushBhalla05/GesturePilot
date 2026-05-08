"""
GesturePilot - Phase 1: Complete Integration
Author: Your Name
Description: Integrates Camera, Person Detection, and Hand Detection
"""

import cv2
import sys
from camera_manager import CameraManager
from person_detector import PersonDetector
from hand_detector import HandDetector

class GesturePilotPhase1:
    """
    Main application class for Phase 1
    Integrates camera, person detection, and hand detection
    """
    
    def __init__(self):
        """Initialize all components"""
        print("=" * 60)
        print("🚀 GESTUREPILOT - PHASE 1: CORE ENGINE")
        print("=" * 60)
        
        # Initialize components
        self.camera = None
        self.person_detector = None
        self.hand_detector = None
        
        # State variables
        self.is_running = False
        self.show_person_skeleton = False  # Toggle with 'p' key
        self.show_hand_skeleton = True     # Toggle with 'h' key
        
        print("\n📦 Initializing components...")
    
    def initialize(self):
        """
        Initialize all components
        
        Returns:
            bool: True if successful
        """
        try:
            # Initialize camera
            print("\n1️⃣ Initializing Camera...")
            self.camera = CameraManager(width=1280, height=720, fps=30)
            if not self.camera.initialize_camera():
                print("❌ Camera initialization failed!")
                return False
            
            # Initialize person detector
            print("\n2️⃣ Initializing Person Detector...")
            self.person_detector = PersonDetector(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            # Initialize hand detector
            print("\n3️⃣ Initializing Hand Detector...")
            self.hand_detector = HandDetector(
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            
            print("\n✅ All components initialized successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Initialization error: {e}")
            return False
    
    def process_frame(self, frame_rgb, frame_bgr, fps):
        """
        Process a single frame through the detection pipeline
        
        Args:
            frame_rgb (numpy.ndarray): Frame in RGB format
            frame_bgr (numpy.ndarray): Frame in BGR format
            fps (float): Current FPS
            
        Returns:
            numpy.ndarray: Processed frame with visualizations
        """
        # Step 1: Validate single person
        is_valid_person, person_msg, person_data = \
            self.person_detector.validate_single_person(frame_rgb)
        
        # Step 2: Detect hands (only if valid person)
        hands_data = []
        hand_results = None
        if is_valid_person:
            hand_results = self.hand_detector.detect_hands(frame_rgb)
            hands_data = self.hand_detector.get_hand_landmarks(hand_results)
        
        # Step 3: Draw visualizations
        
        # Draw person skeleton (optional)
        if self.show_person_skeleton and person_data:
            _, _, person_results = self.person_detector.detect_person(frame_rgb)
            frame_bgr = self.person_detector.draw_person_skeleton(
                frame_bgr, person_results
            )
        
        # Draw hand skeleton
        if self.show_hand_skeleton and hand_results:
            frame_bgr = self.hand_detector.draw_hand_skeleton(
                frame_bgr, hand_results
            )
        
        # Draw hand info
        if hands_data:
            frame_bgr = self.hand_detector.draw_hand_info(
                frame_bgr, hands_data
            )
        
        # Draw status message
        frame_bgr = self.person_detector.draw_status_message(
            frame_bgr, person_msg, is_valid_person
        )
        
        # Draw UI elements
        frame_bgr = self._draw_ui(frame_bgr, fps, is_valid_person, hands_data)
        
        return frame_bgr
    
    def _draw_ui(self, frame_bgr, fps, is_valid_person, hands_data):
        """
        Draw UI elements on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame
            fps (float): Current FPS
            is_valid_person (bool): Person validation status
            hands_data (list): Detected hands data
            
        Returns:
            numpy.ndarray: Frame with UI elements
        """
        h, w = frame_bgr.shape[:2]
        
        # Draw dark semi-transparent overlay for status bar
        overlay = frame_bgr.copy()
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame_bgr, 0.4, 0, frame_bgr)
        
        # FPS counter (top-left)
        fps_color = (0, 255, 0) if fps > 25 else (0, 165, 255)
        cv2.putText(frame_bgr, f"FPS: {int(fps)}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, fps_color, 3)
        
        # Person status (top-center)
        person_color = (0, 255, 0) if is_valid_person else (0, 0, 255)
        person_icon = "✓" if is_valid_person else "✗"
        cv2.putText(frame_bgr, f"Person: {person_icon}", (w//2 - 100, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, person_color, 2)
        
        # Hand count (top-right)
        hand_color = (0, 255, 0) if hands_data else (150, 150, 150)
        cv2.putText(frame_bgr, f"Hands: {len(hands_data)}", (w - 250, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, hand_color, 3)
        
        # Hand details (below hand count)
        if hands_data:
            y_offset = 80
            for hand in hands_data:
                hand_type = hand['hand_type']
                confidence = hand['confidence']
                color = (0, 0, 255) if hand_type == 'Right' else (255, 0, 0)
                
                text = f"{hand_type}: {confidence:.0%}"
                cv2.putText(frame_bgr, text, (w - 250, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_offset += 35
        
        # Draw controls info (bottom)
        controls = [
            "Controls:",
            "'Q' - Quit",
            "'H' - Toggle Hand Skeleton",
            "'P' - Toggle Person Skeleton",
            "'SPACE' - Pause"
        ]
        
        y_start = h - 180
        for i, control in enumerate(controls):
            cv2.putText(frame_bgr, control, (20, y_start + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Draw status indicator (bottom-right)
        status_text = "ACTIVE" if self.is_running else "PAUSED"
        status_color = (0, 255, 0) if self.is_running else (0, 165, 255)
        cv2.putText(frame_bgr, status_text, (w - 180, h - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, status_color, 2)
        
        return frame_bgr
    
    def run(self):
        """
        Main application loop
        """
        if not self.initialize():
            print("\n❌ Failed to initialize. Exiting...")
            return
        
        print("\n" + "=" * 60)
        print("🎬 STARTING DETECTION")
        print("=" * 60)
        print("\n📹 Camera feed starting...")
        print("\n⌨️  CONTROLS:")
        print("   Q     - Quit")
        print("   H     - Toggle Hand Skeleton")
        print("   P     - Toggle Person Skeleton")
        print("   SPACE - Pause/Resume")
        print("\n" + "=" * 60 + "\n")
        
        self.is_running = True
        frame_count = 0
        paused = False
        
        try:
            while True:
                # Get frame
                success, frame_rgb, fps = self.camera.get_frame()
                
                if not success:
                    print("⚠️ Failed to get frame")
                    continue
                
                # Convert to BGR for display
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                
                # Process frame (if not paused)
                if not paused:
                    frame_bgr = self.process_frame(frame_rgb, frame_bgr, fps)
                else:
                    # Draw paused indicator
                    h, w = frame_bgr.shape[:2]
                    cv2.putText(frame_bgr, "PAUSED", (w//2 - 100, h//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 165, 255), 4)
                
                # Display frame
                cv2.imshow("GesturePilot - Phase 1", frame_bgr)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # 'q' or ESC
                    print("\n🛑 Quit requested...")
                    break
                
                elif key == ord('h'):  # Toggle hand skeleton
                    self.show_hand_skeleton = not self.show_hand_skeleton
                    status = "ON" if self.show_hand_skeleton else "OFF"
                    print(f"🤚 Hand skeleton: {status}")
                
                elif key == ord('p'):  # Toggle person skeleton
                    self.show_person_skeleton = not self.show_person_skeleton
                    status = "ON" if self.show_person_skeleton else "OFF"
                    print(f"🧍 Person skeleton: {status}")
                
                elif key == ord(' '):  # Space - pause/resume
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMED"
                    print(f"⏸️  {status}")
                
                frame_count += 1
                
                # Print stats every 100 frames
                if frame_count % 100 == 0:
                    print(f"📊 Processed {frame_count} frames | FPS: {int(fps)}")
        
        except KeyboardInterrupt:
            print("\n⚠️ Keyboard interrupt received...")
        
        except Exception as e:
            print(f"\n❌ Error in main loop: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Cleanup resources
        """
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
        print("👋 GESTUREPILOT PHASE 1 - STOPPED")
        print("=" * 60)


def main():
    """
    Entry point
    """
    app = GesturePilotPhase1()
    app.run()


if __name__ == "__main__":
    main()