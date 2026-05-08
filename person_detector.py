"""
GesturePilot - Phase 1: Person Detector
Author: Your Name
Description: Detects persons using MediaPipe Pose to validate single person requirement
"""

import cv2
import mediapipe as mp
import numpy as np

class PersonDetector:
    """
    Detects persons in frame and validates single person requirement
    """
    
    def __init__(self,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5,
                 model_complexity=1):
        """
        Initialize person detector with MediaPipe Pose
        
        Args:
            min_detection_confidence (float): Minimum confidence for detection
            min_tracking_confidence (float): Minimum confidence for tracking
            model_complexity (int): Model complexity (0=lite, 1=full, 2=heavy)
        """
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Create Pose object
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        print("🧍 Person Detector initialized")
        print(f"   Detection confidence: {min_detection_confidence}")
        print(f"   Tracking confidence: {min_tracking_confidence}")
    
    def detect_person(self, frame_rgb):
        """
        Detect person in the frame
        
        Args:
            frame_rgb (numpy.ndarray): Frame in RGB format
            
        Returns:
            tuple: (person_detected, person_data, results)
                person_detected (bool): Whether person is detected
                person_data (dict): Person information
                results: MediaPipe results object
        """
        # Process the frame
        results = self.pose.process(frame_rgb)
        
        # Check if person detected
        person_detected = results.pose_landmarks is not None
        
        person_data = None
        if person_detected:
            person_data = {
                'landmarks': results.pose_landmarks,
                'confidence': self._get_average_visibility(results.pose_landmarks)
            }
        
        return person_detected, person_data, results
    
    def _get_average_visibility(self, landmarks):
        """
        Calculate average visibility of landmarks
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            float: Average visibility (0-1)
        """
        if not landmarks:
            return 0.0
        
        total_visibility = sum([lm.visibility for lm in landmarks.landmark])
        avg_visibility = total_visibility / len(landmarks.landmark)
        
        return avg_visibility
    
    def get_person_bounding_box(self, landmarks, frame_shape):
        """
        Get bounding box around person
        
        Args:
            landmarks: Pose landmarks
            frame_shape (tuple): (height, width, channels)
            
        Returns:
            tuple: (x, y, w, h) bounding box in pixels
        """
        if not landmarks:
            return None
        
        h, w = frame_shape[:2]
        
        # Get all landmark coordinates
        x_coords = [lm.x * w for lm in landmarks.landmark]
        y_coords = [lm.y * h for lm in landmarks.landmark]
        
        # Calculate bounding box
        x_min = int(min(x_coords))
        x_max = int(max(x_coords))
        y_min = int(min(y_coords))
        y_max = int(max(y_coords))
        
        # Add padding
        padding = 50
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)
        
        return (x_min, y_min, x_max - x_min, y_max - y_min)
    
    def validate_single_person(self, frame_rgb):
        """
        Validate that exactly one person is in frame
        This is a simplified version - MediaPipe Pose detects one person at a time
        
        Args:
            frame_rgb (numpy.ndarray): Frame in RGB format
            
        Returns:
            tuple: (is_valid, status_message, person_data)
                is_valid (bool): True if exactly 1 person
                status_message (str): Status description
                person_data (dict): Person information if detected
        """
        person_detected, person_data, results = self.detect_person(frame_rgb)
        
        if not person_detected:
            return False, "No person detected", None
        
        # Check confidence
        if person_data['confidence'] < 0.5:
            return False, "Person detection confidence too low", None
        
        # MediaPipe Pose detects one person at a time
        # For multiple person detection, we would need a different approach
        # (e.g., YOLO, but that's overkill for this project)
        
        return True, "Single person detected", person_data
    
    def draw_person_skeleton(self, frame_bgr, results):
        """
        Draw person skeleton on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame in BGR format
            results: MediaPipe results object
            
        Returns:
            numpy.ndarray: Frame with skeleton drawn
        """
        if not results.pose_landmarks:
            return frame_bgr
        
        # Draw pose landmarks
        self.mp_drawing.draw_landmarks(
            frame_bgr,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        return frame_bgr
    
    def draw_person_info(self, frame_bgr, person_data, frame_shape):
        """
        Draw person information on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame in BGR format
            person_data (dict): Person data
            frame_shape (tuple): Frame dimensions
            
        Returns:
            numpy.ndarray: Frame with info drawn
        """
        if not person_data:
            return frame_bgr
        
        # Get bounding box
        bbox = self.get_person_bounding_box(person_data['landmarks'], frame_shape)
        
        if bbox:
            x, y, w, h = bbox
            # Draw bounding box
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw confidence
            text = f"Person: {person_data['confidence']:.0%}"
            cv2.putText(frame_bgr, text, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame_bgr
    
    def draw_status_message(self, frame_bgr, message, is_valid):
        """
        Draw status message on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame in BGR format
            message (str): Status message
            is_valid (bool): Whether status is valid/error
            
        Returns:
            numpy.ndarray: Frame with message drawn
        """
        h, w = frame_bgr.shape[:2]
        
        # Determine color based on status
        color = (0, 255, 0) if is_valid else (0, 0, 255)
        
        # Draw background rectangle
        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        bg_x1 = (w - text_size[0]) // 2 - 10
        bg_y1 = 100 - 35
        bg_x2 = bg_x1 + text_size[0] + 20
        bg_y2 = 100 + 10
        
        cv2.rectangle(frame_bgr, (bg_x1, bg_y1), (bg_x2, bg_y2), 
                     (0, 0, 0), -1)  # Black background
        cv2.rectangle(frame_bgr, (bg_x1, bg_y1), (bg_x2, bg_y2), 
                     color, 2)  # Colored border
        
        # Draw text
        text_x = (w - text_size[0]) // 2
        cv2.putText(frame_bgr, message, (text_x, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        return frame_bgr
    
    def release(self):
        """
        Release MediaPipe resources
        """
        if self.pose:
            self.pose.close()
            print("🧍 Person Detector released")


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🧍 TESTING PERSON DETECTOR")
    print("=" * 50)
    
    # Import camera manager
    from camera_manager import CameraManager
    
    # Initialize camera
    camera = CameraManager()
    if not camera.initialize_camera():
        print("❌ Failed to initialize camera!")
        exit()
    
    # Initialize person detector
    detector = PersonDetector()
    
    print("\n🎬 Press 'q' to quit")
    print("=" * 50)
    
    # Main loop
    while True:
        # Get frame
        success, frame_rgb, fps = camera.get_frame()
        
        if not success:
            continue
        
        # Validate single person
        is_valid, status_msg, person_data = detector.validate_single_person(frame_rgb)
        
        # Convert to BGR for display
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw person skeleton (if detected)
        if person_data:
            _, _, results = detector.detect_person(frame_rgb)
            frame_bgr = detector.draw_person_skeleton(frame_bgr, results)
            frame_bgr = detector.draw_person_info(frame_bgr, person_data, frame_rgb.shape)
        
        # Draw status message
        frame_bgr = detector.draw_status_message(frame_bgr, status_msg, is_valid)
        
        # Draw FPS
        cv2.putText(frame_bgr, f"FPS: {int(fps)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Print status
        print(f"\r{status_msg}", end=" " * 20)
        
        # Show frame
        cv2.imshow("Person Detection Test", frame_bgr)
        
        # Break on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print("\n\n🛑 Stopping...")
    
    # Cleanup
    detector.release()
    camera.release_camera()
    cv2.destroyAllWindows()
    
    print("✅ Test completed!")