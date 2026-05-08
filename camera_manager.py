"""
GesturePilot - Phase 1: Camera Manager
Author: Your Name
Description: Handles camera initialization, frame capture, and resource management
"""

import cv2
import numpy as np
import time

class CameraManager:
    """
    Manages camera operations including initialization, frame capture,
    and proper resource cleanup
    """
    
    def __init__(self, camera_index=0, width=1280, height=720, fps=30):
        """
        Initialize camera manager
        
        Args:
            camera_index (int): Camera device index (0 for default webcam)
            width (int): Frame width
            height (int): Frame height
            fps (int): Target frames per second
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.is_opened = False
        
        # FPS calculation variables
        self.prev_frame_time = 0
        self.current_fps = 0
        
        print("🎥 Camera Manager initialized")
    
    def initialize_camera(self):
        """
        Initialize and configure camera with optimal settings
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"📹 Opening camera {self.camera_index}...")
            
            # Open camera
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print("❌ Failed to open camera!")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Auto-adjust exposure and focus
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            
            # Verify settings
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"✅ Camera opened successfully!")
            print(f"   Resolution: {actual_width}x{actual_height}")
            print(f"   Target FPS: {actual_fps}")
            
            self.is_opened = True
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization error: {e}")
            return False
    
    def get_frame(self):
        """
        Capture a single frame from camera
        
        Returns:
            tuple: (success, frame, fps)
                success (bool): Whether frame was captured
                frame (numpy.ndarray): The captured frame in RGB format
                fps (float): Current FPS
        """
        if not self.is_opened or self.cap is None:
            return False, None, 0
        
        # Read frame
        ret, frame = self.cap.read()
        
        if not ret:
            print("⚠️ Failed to read frame")
            return False, None, 0
        
        # Convert BGR to RGB (MediaPipe uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Calculate FPS
        current_time = time.time()
        if self.prev_frame_time != 0:
            self.current_fps = 1 / (current_time - self.prev_frame_time)
        self.prev_frame_time = current_time
        
        return True, frame_rgb, self.current_fps
    
    def get_display_frame(self):
        """
        Get frame in BGR format for OpenCV display
        
        Returns:
            tuple: (success, frame_bgr, fps)
        """
        success, frame_rgb, fps = self.get_frame()
        
        if not success:
            return False, None, 0
        
        # Convert back to BGR for display
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        return True, frame_bgr, fps
    
    def adjust_brightness(self, value):
        """
        Adjust camera brightness
        
        Args:
            value (int): Brightness value (-100 to 100)
        """
        if self.cap:
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)
    
    def adjust_contrast(self, value):
        """
        Adjust camera contrast
        
        Args:
            value (int): Contrast value (0 to 100)
        """
        if self.cap:
            self.cap.set(cv2.CAP_PROP_CONTRAST, value)
    
    def release_camera(self):
        """
        Release camera resources properly
        """
        if self.cap is not None:
            print("📹 Releasing camera...")
            self.cap.release()
            self.is_opened = False
            print("✅ Camera released")
    
    def is_camera_opened(self):
        """
        Check if camera is currently opened
        
        Returns:
            bool: Camera status
        """
        return self.is_opened
    
    def get_camera_info(self):
        """
        Get camera information
        
        Returns:
            dict: Camera properties
        """
        if not self.is_opened:
            return None
        
        info = {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.cap.get(cv2.CAP_PROP_FPS)),
            'brightness': int(self.cap.get(cv2.CAP_PROP_BRIGHTNESS)),
            'contrast': int(self.cap.get(cv2.CAP_PROP_CONTRAST)),
        }
        
        return info


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🎥 TESTING CAMERA MANAGER")
    print("=" * 50)
    
    # Create camera manager
    camera = CameraManager()
    
    # Initialize camera
    if camera.initialize_camera():
        print("\n📊 Camera Info:")
        info = camera.get_camera_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        print("\n🎬 Press 'q' to quit\n")
        
        # Display frames
        while True:
            success, frame, fps = camera.get_display_frame()
            
            if success:
                # Draw FPS
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Show frame
                cv2.imshow("Camera Test", frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        camera.release_camera()
        cv2.destroyAllWindows()
    else:
        print("❌ Camera initialization failed!")