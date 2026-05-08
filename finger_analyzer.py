"""
GesturePilot - Phase 2: Finger Analyzer
Author: Your Name
Description: Analyzes hand landmarks to determine finger states (UP/DOWN)
"""

import numpy as np

class FingerAnalyzer:
    """
    Analyzes finger positions and states from hand landmarks
    """
    
    # Landmark indices for each finger
    THUMB = {'tip': 4, 'ip': 3, 'mcp': 2, 'cmc': 1}
    INDEX = {'tip': 8, 'pip': 6, 'mcp': 5}
    MIDDLE = {'tip': 12, 'pip': 10, 'mcp': 9}
    RING = {'tip': 16, 'pip': 14, 'mcp': 13}
    PINKY = {'tip': 20, 'pip': 18, 'mcp': 17}
    WRIST = 0
    
    def __init__(self):
        """Initialize finger analyzer"""
        print("👆 Finger Analyzer initialized")
    
    def analyze_fingers(self, landmarks, hand_type):
        """
        Analyze all fingers and return their states
        
        Args:
            landmarks (list): Hand landmarks (21 points)
            hand_type (str): 'Left' or 'Right'
            
        Returns:
            dict: Finger states
                {
                    'thumb': bool,
                    'index': bool,
                    'middle': bool,
                    'ring': bool,
                    'pinky': bool,
                    'pattern': [0/1, 0/1, 0/1, 0/1, 0/1]
                }
        """
        if not landmarks or len(landmarks) < 21:
            return None
        
        # Check each finger
        thumb_up = self._is_thumb_up(landmarks, hand_type)
        index_up = self._is_finger_up(landmarks, self.INDEX)
        middle_up = self._is_finger_up(landmarks, self.MIDDLE)
        ring_up = self._is_finger_up(landmarks, self.RING)
        pinky_up = self._is_finger_up(landmarks, self.PINKY)
        
        # Create pattern array [thumb, index, middle, ring, pinky]
        pattern = [
            1 if thumb_up else 0,
            1 if index_up else 0,
            1 if middle_up else 0,
            1 if ring_up else 0,
            1 if pinky_up else 0
        ]
        
        return {
            'thumb': thumb_up,
            'index': index_up,
            'middle': middle_up,
            'ring': ring_up,
            'pinky': pinky_up,
            'pattern': pattern,
            'hand_type': hand_type
        }
    
    def _is_finger_up(self, landmarks, finger_indices):
        """
        Check if a finger (except thumb) is extended/up
        
        Args:
            landmarks (list): Hand landmarks
            finger_indices (dict): Finger landmark indices
            
        Returns:
            bool: True if finger is up
        """
        tip = landmarks[finger_indices['tip']]
        pip = landmarks[finger_indices['pip']]
        mcp = landmarks[finger_indices['mcp']]
        
        # Finger is UP if tip is above pip and pip is above mcp
        # (Y coordinate decreases as we go up)
        return tip['y'] < pip['y'] < mcp['y']
    
    def _is_thumb_up(self, landmarks, hand_type):
        """
        Check if thumb is extended (special case)
        
        Args:
            landmarks (list): Hand landmarks
            hand_type (str): 'Left' or 'Right'
            
        Returns:
            bool: True if thumb is up/extended
        """
        thumb_tip = landmarks[self.THUMB['tip']]
        thumb_ip = landmarks[self.THUMB['ip']]
        thumb_mcp = landmarks[self.THUMB['mcp']]
        
        # Thumb moves horizontally (X-axis) more than vertically
        # For right hand: thumb extended means tip.x < ip.x
        # For left hand: thumb extended means tip.x > ip.x
        
        if hand_type.lower() == 'right':
            # Right hand: thumb goes left when extended
            return thumb_tip['x'] < thumb_ip['x'] < thumb_mcp['x']
        else:
            # Left hand: thumb goes right when extended
            return thumb_tip['x'] > thumb_ip['x'] > thumb_mcp['x']
    
    def get_finger_count(self, finger_states):
        """
        Count number of extended fingers
        
        Args:
            finger_states (dict): Finger states from analyze_fingers()
            
        Returns:
            int: Number of fingers up (0-5)
        """
        if not finger_states:
            return 0
        
        count = sum([
            finger_states['thumb'],
            finger_states['index'],
            finger_states['middle'],
            finger_states['ring'],
            finger_states['pinky']
        ])
        
        return count
    
    def pattern_to_string(self, pattern):
        """
        Convert pattern to readable string
        
        Args:
            pattern (list): [0/1, 0/1, 0/1, 0/1, 0/1]
            
        Returns:
            str: Pattern representation
        """
        fingers = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        up_fingers = [fingers[i] for i, state in enumerate(pattern) if state == 1]
        
        if not up_fingers:
            return "Fist (all down)"
        elif len(up_fingers) == 5:
            return "Open Palm (all up)"
        else:
            return " + ".join(up_fingers)
    
    def is_fist(self, finger_states):
        """
        Check if hand is making a fist
        
        Args:
            finger_states (dict): Finger states
            
        Returns:
            bool: True if fist
        """
        if not finger_states:
            return False
        
        return sum(finger_states['pattern']) == 0
    
    def is_open_palm(self, finger_states):
        """
        Check if hand is open palm
        
        Args:
            finger_states (dict): Finger states
            
        Returns:
            bool: True if open palm
        """
        if not finger_states:
            return False
        
        return sum(finger_states['pattern']) == 5
    
    def get_extended_fingers(self, finger_states):
        """
        Get list of extended finger names
        
        Args:
            finger_states (dict): Finger states
            
        Returns:
            list: Names of extended fingers
        """
        if not finger_states:
            return []
        
        extended = []
        if finger_states['thumb']:
            extended.append('thumb')
        if finger_states['index']:
            extended.append('index')
        if finger_states['middle']:
            extended.append('middle')
        if finger_states['ring']:
            extended.append('ring')
        if finger_states['pinky']:
            extended.append('pinky')
        
        return extended
    
    def calculate_finger_angles(self, landmarks):
        """
        Calculate angles for each finger (advanced)
        
        Args:
            landmarks (list): Hand landmarks
            
        Returns:
            dict: Angles for each finger
        """
        def get_angle(p1, p2, p3):
            """Calculate angle between three points"""
            v1 = np.array([p1['x'] - p2['x'], p1['y'] - p2['y']])
            v2 = np.array([p3['x'] - p2['x'], p3['y'] - p2['y']])
            
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
            angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
            
            return np.degrees(angle)
        
        angles = {}
        
        # Index finger angle
        angles['index'] = get_angle(
            landmarks[self.INDEX['tip']],
            landmarks[self.INDEX['pip']],
            landmarks[self.INDEX['mcp']]
        )
        
        # Middle finger angle
        angles['middle'] = get_angle(
            landmarks[self.MIDDLE['tip']],
            landmarks[self.MIDDLE['pip']],
            landmarks[self.MIDDLE['mcp']]
        )
        
        # Ring finger angle
        angles['ring'] = get_angle(
            landmarks[self.RING['tip']],
            landmarks[self.RING['pip']],
            landmarks[self.RING['mcp']]
        )
        
        # Pinky finger angle
        angles['pinky'] = get_angle(
            landmarks[self.PINKY['tip']],
            landmarks[self.PINKY['pip']],
            landmarks[self.PINKY['mcp']]
        )
        
        return angles


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("👆 TESTING FINGER ANALYZER")
    print("=" * 50)
    
    # Test with sample landmarks
    # Simulate "peace sign" - index and middle up
    sample_landmarks = [
        # ... (would need full 21 landmarks)
        # This is just for structure demonstration
    ]
    
    analyzer = FingerAnalyzer()
    
    # Simulate different gestures
    print("\nTest Case 1: Index finger only")
    test_pattern = [0, 1, 0, 0, 0]  # Only index up
    print(f"Pattern: {test_pattern}")
    print(f"Readable: {analyzer.pattern_to_string(test_pattern)}")
    
    print("\nTest Case 2: Peace sign")
    test_pattern = [0, 1, 1, 0, 0]  # Index and middle up
    print(f"Pattern: {test_pattern}")
    print(f"Readable: {analyzer.pattern_to_string(test_pattern)}")
    
    print("\nTest Case 3: Open palm")
    test_pattern = [1, 1, 1, 1, 1]  # All fingers up
    print(f"Pattern: {test_pattern}")
    print(f"Readable: {analyzer.pattern_to_string(test_pattern)}")
    
    print("\nTest Case 4: Fist")
    test_pattern = [0, 0, 0, 0, 0]  # All fingers down
    print(f"Pattern: {test_pattern}")
    print(f"Readable: {analyzer.pattern_to_string(test_pattern)}")
    
    print("\n✅ Finger Analyzer tests completed!")