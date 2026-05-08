"""
GesturePilot - Phase 5: History Manager
Author: Your Name
Description: Manages gesture action history (last 100 actions)
"""

import json
import csv
from datetime import datetime
from collections import deque, Counter
from pathlib import Path

class HistoryManager:
    """
    Manages gesture action history with statistics
    """
    
    def __init__(self, max_size=100, history_file='logs/gesture_history.json'):
        """
        Initialize history manager
        
        Args:
            max_size (int): Maximum number of actions to store
            history_file (str): Path to history file
        """
        self.max_size = max_size
        self.history_file = Path(history_file)
        self.history = deque(maxlen=max_size)
        
        # Create logs directory
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        self.load_history()
        
        print(f"📊 History Manager initialized (Max: {max_size})")
    
    def add_action(self, gesture_name, action_name, hand_type, 
                   confidence=0, status='success'):
        """
        Add action to history
        
        Args:
            gesture_name (str): Gesture name
            action_name (str): Action executed
            hand_type (str): 'left' or 'right'
            confidence (float): Detection confidence
            status (str): 'success' or 'failed'
        """
        entry = {
            'id': len(self.history) + 1,
            'timestamp': datetime.now().isoformat(),
            'datetime_readable': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'gesture': gesture_name,
            'action': action_name,
            'hand': hand_type,
            'confidence': round(confidence, 1),
            'status': status
        }
        
        self.history.append(entry)
        
        # Auto-save every 10 actions
        if len(self.history) % 10 == 0:
            self.save_history()
    
    def get_history(self, limit=None):
        """
        Get history entries
        
        Args:
            limit (int, optional): Number of recent entries
        
        Returns:
            list: History entries
        """
        if limit:
            return list(self.history)[-limit:]
        return list(self.history)
    
    def get_statistics(self):
        """
        Calculate statistics from history
        
        Returns:
            dict: Statistics
        """
        if not self.history:
            return {
                'total': 0,
                'success': 0,
                'failed': 0,
                'success_rate': 0,
                'most_used_gesture': 'None',
                'most_used_action': 'None',
                'gestures_per_hand': {'left': 0, 'right': 0},
                'recent_activity': []
            }
        
        # Count statuses
        success_count = sum(1 for e in self.history if e['status'] == 'success')
        failed_count = len(self.history) - success_count
        success_rate = (success_count / len(self.history)) * 100
        
        # Most used gesture
        gestures = [e['gesture'] for e in self.history]
        most_used_gesture = Counter(gestures).most_common(1)[0][0] if gestures else 'None'
        
        # Most used action
        actions = [e['action'] for e in self.history]
        most_used_action = Counter(actions).most_common(1)[0][0] if actions else 'None'
        
        # Gestures per hand
        left_count = sum(1 for e in self.history if e['hand'].lower() == 'left')
        right_count = len(self.history) - left_count
        
        # Recent activity (last 5)
        recent = list(self.history)[-5:]
        
        return {
            'total': len(self.history),
            'success': success_count,
            'failed': failed_count,
            'success_rate': round(success_rate, 1),
            'most_used_gesture': most_used_gesture,
            'most_used_action': most_used_action,
            'gestures_per_hand': {
                'left': left_count,
                'right': right_count
            },
            'recent_activity': recent
        }
    
    def get_gesture_counts(self):
        """
        Get count of each gesture
        
        Returns:
            dict: Gesture counts
        """
        gestures = [e['gesture'] for e in self.history]
        return dict(Counter(gestures))
    
    def get_action_counts(self):
        """
        Get count of each action
        
        Returns:
            dict: Action counts
        """
        actions = [e['action'] for e in self.history]
        return dict(Counter(actions))
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.save_history()
        print("🗑️ History cleared")
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            data = {
                'max_size': self.max_size,
                'count': len(self.history),
                'last_updated': datetime.now().isoformat(),
                'history': list(self.history)
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"⚠️ Failed to save history: {e}")
    
    def load_history(self):
        """Load history from JSON file"""
        try:
            if not self.history_file.exists():
                print("📝 No existing history found")
                return
            
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            history_list = data.get('history', [])
            self.history = deque(history_list, maxlen=self.max_size)
            
            print(f"✅ Loaded {len(self.history)} history entries")
            
        except Exception as e:
            print(f"⚠️ Failed to load history: {e}")
            self.history = deque(maxlen=self.max_size)
    
    def export_to_csv(self, filename='gesture_history.csv'):
        """
        Export history to CSV file
        
        Args:
            filename (str): Output filename
        
        Returns:
            bool: Success status
        """
        try:
            if not self.history:
                print("⚠️ No history to export")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'datetime', 'gesture', 'action', 
                             'hand', 'confidence', 'status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for entry in self.history:
                    writer.writerow({
                        'id': entry['id'],
                        'datetime': entry['datetime_readable'],
                        'gesture': entry['gesture'],
                        'action': entry['action'],
                        'hand': entry['hand'],
                        'confidence': entry['confidence'],
                        'status': entry['status']
                    })
            
            print(f"📥 History exported to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def get_hourly_activity(self):
        """
        Get activity count per hour (last 24 hours)
        
        Returns:
            dict: Hour -> count mapping
        """
        activity = {}
        now = datetime.now()
        
        for entry in self.history:
            try:
                entry_time = datetime.fromisoformat(entry['timestamp'])
                hour_diff = int((now - entry_time).total_seconds() / 3600)
                
                if hour_diff < 24:
                    hour_key = f"{hour_diff}h ago"
                    activity[hour_key] = activity.get(hour_key, 0) + 1
            except:
                continue
        
        return activity


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("📊 TESTING HISTORY MANAGER")
    print("=" * 50)
    
    # Create history manager
    history = HistoryManager(max_size=10)
    
    # Add test actions
    print("\n🧪 Adding test actions...")
    history.add_action("One Finger (Right)", "open_youtube", "right", 85.5, "success")
    history.add_action("Two Fingers (Right)", "music_play_pause", "right", 90.2, "success")
    history.add_action("Open Palm (Left)", "minimize_all", "left", 78.9, "success")
    history.add_action("Fist (Right)", "stop_action", "right", 95.1, "failed")
    
    # Get statistics
    print("\n📈 Statistics:")
    stats = history.get_statistics()
    for key, value in stats.items():
        if key != 'recent_activity':
            print(f"   {key}: {value}")
    
    # Get history
    print("\n📋 Recent History:")
    for entry in history.get_history(limit=5):
        print(f"   {entry['datetime_readable']} - {entry['gesture']} -> {entry['action']}")
    
    # Export to CSV
    print("\n📥 Exporting to CSV...")
    history.export_to_csv('test_history.csv')
    
    print("\n✅ History Manager tests completed!")