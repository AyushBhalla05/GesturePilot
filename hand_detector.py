"""
GesturePilot - Phase 1: Hand Detector
Author: Your Name
Description: Detects hands using MediaPipe, classifies left/right, extracts landmarks
"""

import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    """
    Handles hand detection, tracking, and landmark extraction using MediaPipe
    """
    
    def __init__(self, 
                 max_num_hands=2,
                 min_detection_confidence=0.8,
                 min_tracking_confidence=0.8,
                 model_complexity=1):
        """
        Initialize hand detector with MediaPipe
        
        Args:
            max_num_hands (int): Maximum number of hands to detect
            min_detection_confidence (float): Minimum confidence for detection
            min_tracking_confidence (float): Minimum confidence for tracking
            model_complexity (int): Model complexity (0=lite, 1=full)
        """
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Create Hands object
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=model_complexity
        )
        
        # Hand landmarks indices
        self.WRIST = 0
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20
        
        print("🤚 Hand Detector initialized")
        print(f"   Max hands: {max_num_hands}")
        print(f"   Detection confidence: {min_detection_confidence}")
        print(f"   Tracking confidence: {min_tracking_confidence}")
    
    def detect_hands(self, frame_rgb):
        """
        Detect hands in the frame
        
        Args:
            frame_rgb (numpy.ndarray): Frame in RGB format
            
        Returns:
            object: MediaPipe results object
        """
        # Process the frame
        results = self.hands.process(frame_rgb)
        return results
    
    def get_hand_landmarks(self, results):
        """
        Extract hand landmarks from results
        
        Args:
            results: MediaPipe results object
            
        Returns:
            list: List of hand data dictionaries
                Each dict contains:
                - 'hand_type': 'Left' or 'Right'
                - 'landmarks': List of 21 (x, y, z) coordinates
                - 'landmarks_px': List of 21 (x, y) pixel coordinates
        """
        if not results.multi_hand_landmarks:
            return []
        
        hands_data = []
        
        # Get image dimensions (assume from first landmark)
        if results.multi_hand_landmarks:
            # We'll get image dimensions when drawing
            pass
        
        # Process each detected hand
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand classification (Left or Right)
            hand_type = results.multi_handedness[idx].classification[0].label
            
            # Extract landmarks (normalized coordinates 0-1)
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
            
            hands_data.append({
                'hand_type': hand_type,
                'landmarks': landmarks,
                'confidence': results.multi_handedness[idx].classification[0].score
            })
        
        return hands_data
    
    def get_landmarks_pixels(self, landmarks, frame_shape):
        """
        Convert normalized landmarks to pixel coordinates
        
        Args:
            landmarks (list): Normalized landmarks (0-1)
            frame_shape (tuple): (height, width, channels)
            
        Returns:
            list: Pixel coordinates [(x, y), ...]
        """
        h, w = frame_shape[:2]
        landmarks_px = []
        
        for lm in landmarks:
            x_px = int(lm['x'] * w)
            y_px = int(lm['y'] * h)
            landmarks_px.append((x_px, y_px))
        
        return landmarks_px
    
    def draw_hand_skeleton(self, frame_bgr, results):
        """
        Draw hand skeleton on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame in BGR format
            results: MediaPipe results object
            
        Returns:
            numpy.ndarray: Frame with skeleton drawn
        """
        if not results.multi_hand_landmarks:
            return frame_bgr
        
        # Draw each hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections
            self.mp_drawing.draw_landmarks(
                frame_bgr,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return frame_bgr
    
    def draw_hand_info(self, frame_bgr, hands_data):
        """
        Draw hand information (type, confidence) on frame
        
        Args:
            frame_bgr (numpy.ndarray): Frame in BGR format
            hands_data (list): List of hand data dictionaries
            
        Returns:
            numpy.ndarray: Frame with info drawn
        """
        h, w = frame_bgr.shape[:2]
        
        for idx, hand in enumerate(hands_data):
            # Get wrist position for text placement
            wrist = hand['landmarks'][self.WRIST]
            x_px = int(wrist['x'] * w)
            y_px = int(wrist['y'] * h)
            
            # Determine color based on hand type
            if hand['hand_type'] == 'Right':
                color = (0, 0, 255)  # Red for right hand
            else:
                color = (255, 0, 0)  # Blue for left hand
            
            # Draw hand type
            text = f"{hand['hand_type']} ({hand['confidence']:.0%})"
            cv2.putText(frame_bgr, text, (x_px - 50, y_px - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame_bgr
    
    def classify_hand_side(self, landmarks):
        """
        Classify if hand is left or right based on landmark positions
        (Backup method if MediaPipe classification fails)
        
        Args:
            landmarks (list): Hand landmarks
            
        Returns:
            str: 'Left' or 'Right'
        """
        # Compare thumb and pinky positions
        thumb_x = landmarks[self.THUMB_TIP]['x']
        pinky_x = landmarks[self.PINKY_TIP]['x']
        
        # If thumb is to the right of pinky, it's a right hand
        if thumb_x > pinky_x:
            return 'Right'
        else:
            return 'Left'
    
    def get_hand_center(self, landmarks):
        """
        Calculate center point of hand (average of all landmarks)
        
        Args:
            landmarks (list): Hand landmarks
            
        Returns:
            tuple: (x, y) normalized coordinates
        """
        x_avg = sum([lm['x'] for lm in landmarks]) / len(landmarks)
        y_avg = sum([lm['y'] for lm in landmarks]) / len(landmarks)
        
        return (x_avg, y_avg)
    
    def is_hand_stable(self, landmarks, prev_landmarks, threshold=0.05):
        """
        Check if hand is stable (not moving too much)
        
        Args:
            landmarks (list): Current landmarks
            prev_landmarks (list): Previous frame landmarks
            threshold (float): Movement threshold
            
        Returns:
            bool: True if hand is stable
        """
        if prev_landmarks is None:
            return False
        
        # Calculate average movement of key points
        key_points = [self.WRIST, self.THUMB_TIP, self.INDEX_TIP, 
                     self.MIDDLE_TIP, self.RING_TIP, self.PINKY_TIP]
        
        total_movement = 0
        for idx in key_points:
            dx = landmarks[idx]['x'] - prev_landmarks[idx]['x']
            dy = landmarks[idx]['y'] - prev_landmarks[idx]['y']
            movement = np.sqrt(dx**2 + dy**2)
            total_movement += movement
        
        avg_movement = total_movement / len(key_points)
        
        return avg_movement < threshold
    
    def release(self):
        """
        Release MediaPipe resources
        """
        if self.hands:
            self.hands.close()
            print("🤚 Hand Detector released")


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🤚 TESTING HAND DETECTOR")
    print("=" * 50)
    
    # Import camera manager
    from camera_manager import CameraManager
    
    # Initialize camera
    camera = CameraManager()
    if not camera.initialize_camera():
        print("❌ Failed to initialize camera!")
        exit()
    
    # Initialize hand detector
    detector = HandDetector(max_num_hands=2)
    
    print("\n🎬 Press 'q' to quit")
    print("=" * 50)
    
    # Main loop
    while True:
        # Get frame
        success, frame_rgb, fps = camera.get_frame()
        
        if not success:
            continue
        
        # Detect hands
        results = detector.detect_hands(frame_rgb)
        
        # Get hand data
        hands_data = detector.get_hand_landmarks(results)
        
        # Convert to BGR for display
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw skeleton
        frame_bgr = detector.draw_hand_skeleton(frame_bgr, results)
        
        # Draw hand info
        frame_bgr = detector.draw_hand_info(frame_bgr, hands_data)
        
        # Draw FPS
        cv2.putText(frame_bgr, f"FPS: {int(fps)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw hand count
        cv2.putText(frame_bgr, f"Hands: {len(hands_data)}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Print hand info
        if hands_data:
            for idx, hand in enumerate(hands_data):
                print(f"\r{hand['hand_type']} Hand | "
                      f"Confidence: {hand['confidence']:.0%} | "
                      f"Landmarks: {len(hand['landmarks'])}", end="")
        else:
            print("\rNo hands detected" + " " * 50, end="")
        
        # Show frame
        cv2.imshow("Hand Detection Test", frame_bgr)
        
        # Break on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print("\n\n🛑 Stopping...")
    
    # Cleanup
    detector.release()
    camera.release_camera()
    cv2.destroyAllWindows()
    
    print("✅ Test completed!")