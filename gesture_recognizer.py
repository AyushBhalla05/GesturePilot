"""
GesturePilot - Phase 2: Gesture Recognizer
Author: Your Name
Description: Recognizes gestures from finger patterns with confidence filtering
"""

import json
import time
from collections import deque, Counter

class GestureRecognizer:
    """
    Recognizes gestures from finger patterns and applies confidence filtering
    """
    
    def __init__(self, library_path='gesture_library.json'):
        """
        Initialize gesture recognizer
        
        Args:
            library_path (str): Path to gesture library JSON file
        """
        self.library_path = library_path
        self.gestures = []
        self.settings = {}
        
        # Gesture buffer for temporal smoothing
        self.buffer_size = 30  # 1 second at 30 FPS
        self.gesture_buffer = {
            'left': deque(maxlen=self.buffer_size),
            'right': deque(maxlen=self.buffer_size)
        }
        
        # Cooldown tracking
        self.last_gesture_time = {
            'left': 0,
            'right': 0
        }
        
        # Load gesture library
        self.load_library()
        
        print("🎯 Gesture Recognizer initialized")
        print(f"   Loaded {len(self.gestures)} gestures")
        print(f"   Confidence threshold: {self.settings.get('confidence_threshold', 80)}%")
        print(f"   Cooldown: {self.settings.get('cooldown_seconds', 2.0)}s")
    
    def load_library(self):
        """Load gesture library from JSON file"""
        try:
            with open(self.library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.gestures = data.get('gestures', [])
                self.settings = data.get('settings', {})
                
            # Filter enabled gestures
            self.gestures = [g for g in self.gestures if g.get('enabled', True)]
            
            print(f"✅ Loaded {len(self.gestures)} gestures from {self.library_path}")
            
        except FileNotFoundError:
            print(f"⚠️ Gesture library not found: {self.library_path}")
            print("   Creating default library...")
            self._create_default_library()
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing gesture library: {e}")
            self.gestures = []
            self.settings = {}
        except UnicodeDecodeError as e:
            print(f"❌ Encoding error in gesture library: {e}")
            print("   Tip: Save gesture_library.json with UTF-8 encoding")
            self.gestures = []
            self.settings = {}
    
    def _create_default_library(self):
        """Create a minimal default gesture library"""
        default_data = {
            "version": "1.0",
            "gestures": [
                {
                    "id": "right_one_finger",
                    "name": "One Finger (Right)",
                    "hand": "right",
                    "pattern": [0, 1, 0, 0, 0],
                    "action": "open_youtube",
                    "enabled": True
                }
            ],
            "settings": {
                "confidence_threshold": 80,
                "stability_frames": 15,
                "cooldown_seconds": 2.0
            }
        }
        
        try:
            with open(self.library_path, 'w') as f:
                json.dump(default_data, f, indent=2)
            print(f"✅ Created default library: {self.library_path}")
            self.load_library()
        except Exception as e:
            print(f"❌ Could not create default library: {e}")
    
    def match_gesture(self, finger_states):
        """
        Match finger pattern against gesture library
        
        Args:
            finger_states (dict): Finger states from FingerAnalyzer
                Must contain: 'pattern' and 'hand_type'
        
        Returns:
            dict or None: Matched gesture data or None
        """
        if not finger_states or 'pattern' not in finger_states:
            return None
        
        pattern = finger_states['pattern']
        hand_type = finger_states['hand_type'].lower()
        
        # Search for matching gesture
        for gesture in self.gestures:
            if gesture['hand'] == hand_type and gesture['pattern'] == pattern:
                return gesture
        
        return None
    
    def add_to_buffer(self, hand_type, gesture_id):
        """
        Add gesture to temporal buffer
        
        Args:
            hand_type (str): 'left' or 'right'
            gesture_id (str): Gesture ID or 'none'
        """
        hand_key = hand_type.lower()
        if hand_key in self.gesture_buffer:
            self.gesture_buffer[hand_key].append(gesture_id if gesture_id else 'none')
    
    def get_stable_gesture(self, hand_type):
        """
        Get stable gesture after applying temporal filter
        
        Args:
            hand_type (str): 'left' or 'right'
        
        Returns:
            tuple: (gesture_id, confidence) or (None, 0)
        """
        hand_key = hand_type.lower()
        buffer = self.gesture_buffer.get(hand_key, [])
        
        if len(buffer) < self.settings.get('stability_frames', 15):
            return None, 0
        
        # Count occurrences
        counts = Counter(buffer)
        
        # Remove 'none' from consideration
        if 'none' in counts:
            del counts['none']
        
        if not counts:
            return None, 0
        
        # Get most common gesture
        most_common = counts.most_common(1)[0]
        gesture_id, count = most_common
        
        # Calculate confidence
        confidence = (count / len(buffer)) * 100
        
        # Check if meets threshold
        threshold = self.settings.get('confidence_threshold', 80)
        if confidence >= threshold:
            return gesture_id, confidence
        
        return None, confidence
    
    def is_cooldown_active(self, hand_type):
        """
        Check if cooldown is active for a hand
        
        Args:
            hand_type (str): 'left' or 'right'
        
        Returns:
            bool: True if cooldown is active
        """
        hand_key = hand_type.lower()
        cooldown_duration = self.settings.get('cooldown_seconds', 2.0)
        
        last_time = self.last_gesture_time.get(hand_key, 0)
        elapsed = time.time() - last_time
        
        return elapsed < cooldown_duration
    
    def update_cooldown(self, hand_type):
        """
        Update last gesture time for cooldown
        
        Args:
            hand_type (str): 'left' or 'right'
        """
        hand_key = hand_type.lower()
        self.last_gesture_time[hand_key] = time.time()
    
    def get_cooldown_remaining(self, hand_type):
        """
        Get remaining cooldown time
        
        Args:
            hand_type (str): 'left' or 'right'
        
        Returns:
            float: Remaining seconds (0 if no cooldown)
        """
        hand_key = hand_type.lower()
        cooldown_duration = self.settings.get('cooldown_seconds', 2.0)
        
        last_time = self.last_gesture_time.get(hand_key, 0)
        elapsed = time.time() - last_time
        remaining = max(0, cooldown_duration - elapsed)
        
        return remaining
    
    def recognize_gesture(self, finger_states):
        """
        Full gesture recognition pipeline
        
        Args:
            finger_states (dict): Finger states from FingerAnalyzer
        
        Returns:
            dict: Recognition result
                {
                    'recognized': bool,
                    'gesture': dict or None,
                    'confidence': float,
                    'cooldown_active': bool,
                    'status': str
                }
        """
        result = {
            'recognized': False,
            'gesture': None,
            'confidence': 0,
            'cooldown_active': False,
            'status': 'no_gesture'
        }
        
        if not finger_states:
            return result
        
        hand_type = finger_states.get('hand_type', '').lower()
        
        # Step 1: Match pattern
        matched_gesture = self.match_gesture(finger_states)
        
        if matched_gesture:
            # Step 2: Add to buffer
            self.add_to_buffer(hand_type, matched_gesture['id'])
            
            # Step 3: Check stability
            stable_gesture_id, confidence = self.get_stable_gesture(hand_type)
            
            if stable_gesture_id:
                # Step 4: Check cooldown
                if self.is_cooldown_active(hand_type):
                    result['cooldown_active'] = True
                    result['status'] = 'cooldown'
                    result['confidence'] = confidence
                    return result
                
                # Gesture recognized!
                result['recognized'] = True
                result['gesture'] = matched_gesture
                result['confidence'] = confidence
                result['status'] = 'confirmed'
                
                # Update cooldown
                self.update_cooldown(hand_type)
            else:
                result['confidence'] = confidence
                result['status'] = 'low_confidence'
        else:
            # No match - add 'none' to buffer
            self.add_to_buffer(hand_type, None)
            result['status'] = 'no_match'
        
        return result
    
    def clear_buffer(self, hand_type=None):
        """
        Clear gesture buffer
        
        Args:
            hand_type (str, optional): Specific hand or None for both
        """
        if hand_type:
            hand_key = hand_type.lower()
            if hand_key in self.gesture_buffer:
                self.gesture_buffer[hand_key].clear()
        else:
            for hand_key in self.gesture_buffer:
                self.gesture_buffer[hand_key].clear()
    
    def get_gesture_by_id(self, gesture_id):
        """
        Get gesture data by ID
        
        Args:
            gesture_id (str): Gesture ID
        
        Returns:
            dict or None: Gesture data
        """
        for gesture in self.gestures:
            if gesture['id'] == gesture_id:
                return gesture
        return None
    
    def get_gestures_by_hand(self, hand_type):
        """
        Get all gestures for a specific hand
        
        Args:
            hand_type (str): 'left' or 'right'
        
        Returns:
            list: Gestures for specified hand
        """
        hand_key = hand_type.lower()
        return [g for g in self.gestures if g['hand'] == hand_key]
    
    def get_all_gestures(self):
        """Get all loaded gestures"""
        return self.gestures
    
    def reload_library(self):
        """Reload gesture library from file"""
        print("🔄 Reloading gesture library...")
        self.load_library()


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🎯 TESTING GESTURE RECOGNIZER")
    print("=" * 50)
    
    recognizer = GestureRecognizer()
    
    print("\n📊 Loaded Gestures:")
    for gesture in recognizer.get_all_gestures():
        print(f"   {gesture['icon']} {gesture['name']}: {gesture['pattern']}")
    
    print("\n🧪 Test Case 1: Right hand - One finger")
    test_finger_states = {
        'pattern': [0, 1, 0, 0, 0],
        'hand_type': 'Right'
    }
    
    # Simulate multiple frames for stability
    for i in range(20):
        result = recognizer.recognize_gesture(test_finger_states)
        if result['recognized']:
            print(f"✅ Gesture recognized: {result['gesture']['name']}")
            print(f"   Confidence: {result['confidence']:.1f}%")
            break
    
    print("\n🧪 Test Case 2: Check cooldown")
    result = recognizer.recognize_gesture(test_finger_states)
    if result['cooldown_active']:
        print(f"⏱️ Cooldown active: {recognizer.get_cooldown_remaining('right'):.1f}s remaining")
    
    print("\n✅ Gesture Recognizer tests completed!")