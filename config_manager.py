"""
GesturePilot - Phase 5: Config Manager
Author: Your Name
Description: Manages application configuration and settings
"""

import json
from pathlib import Path

class ConfigManager:
    """
    Manages application configuration
    """
    
    def __init__(self, config_file='config/settings.json'):
        """
        Initialize config manager
        
        Args:
            config_file (str): Path to config file
        """
        self.config_file = Path(config_file)
        self.config = {}
        
        # Create config directory
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing config
        self.load_config()
        
        print("⚙️ Config Manager initialized")
    
    def get_default_config(self):
        """
        Get default configuration
        
        Returns:
            dict: Default config
        """
        return {
            'app': {
                'version': '1.0.0',
                'first_run': True,
                'window_width': 1200,
                'window_height': 850
            },
            'camera': {
                'resolution_width': 1280,
                'resolution_height': 720,
                'fps': 30,
                'camera_index': 0
            },
            'detection': {
                'confidence_threshold': 80,
                'stability_frames': 15,
                'cooldown_duration': 2.0,
                'min_detection_confidence': 0.7,
                'min_tracking_confidence': 0.5
            },
            'ui': {
                'show_skeleton': True,
                'show_fps': True,
                'show_confidence': True,
                'dark_mode': True,
                'voice_feedback': True
            },
            'autostart': {
                'enabled': False
            },
            'advanced': {
                'max_history_size': 100,
                'auto_save_interval': 10,
                'log_level': 'INFO'
            }
        }
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if not self.config_file.exists():
                print("📝 No config file found, using defaults")
                self.config = self.get_default_config()
                self.save_config()
                return
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # Merge with defaults (in case new keys added)
            default_config = self.get_default_config()
            self.config = self._merge_configs(default_config, self.config)
            
            print("✅ Config loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Failed to load config: {e}")
            print("   Using default configuration")
            self.config = self.get_default_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print("💾 Config saved")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    def get(self, key_path, default=None):
        """
        Get config value by key path
        
        Args:
            key_path (str): Dot-separated key path (e.g., 'ui.show_fps')
            default: Default value if key not found
            
        Returns:
            Value at key path or default
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """
        Set config value by key path
        
        Args:
            key_path (str): Dot-separated key path
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set value
        config[keys[-1]] = value
    
    def update(self, updates):
        """
        Update multiple config values
        
        Args:
            updates (dict): Dictionary of updates
        """
        def deep_update(base, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in base:
                    deep_update(base[key], value)
                else:
                    base[key] = value
        
        deep_update(self.config, updates)
    
    def reset_to_default(self):
        """Reset configuration to defaults"""
        self.config = self.get_default_config()
        self.save_config()
        print("🔄 Config reset to defaults")
    
    def _merge_configs(self, default, loaded):
        """
        Merge loaded config with defaults
        
        Args:
            default (dict): Default config
            loaded (dict): Loaded config
            
        Returns:
            dict: Merged config
        """
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_all(self):
        """
        Get entire configuration
        
        Returns:
            dict: Complete configuration
        """
        return self.config.copy()
    
    def export_config(self, filename):
        """
        Export configuration to file
        
        Args:
            filename (str): Export filename
            
        Returns:
            bool: Success status
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"📥 Config exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def import_config(self, filename):
        """
        Import configuration from file
        
        Args:
            filename (str): Import filename
            
        Returns:
            bool: Success status
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            self.config = imported
            self.save_config()
            print(f"📤 Config imported from {filename}")
            return True
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("⚙️ TESTING CONFIG MANAGER")
    print("=" * 50)
    
    # Create config manager
    config = ConfigManager('test_config.json')
    
    # Test get
    print("\n🧪 Test 1: Get values")
    print(f"   FPS: {config.get('camera.fps')}")
    print(f"   Confidence: {config.get('detection.confidence_threshold')}")
    print(f"   Show skeleton: {config.get('ui.show_skeleton')}")
    
    # Test set
    print("\n🧪 Test 2: Set values")
    config.set('camera.fps', 60)
    config.set('ui.voice_feedback', False)
    print(f"   New FPS: {config.get('camera.fps')}")
    print(f"   Voice feedback: {config.get('ui.voice_feedback')}")
    
    # Test update
    print("\n🧪 Test 3: Batch update")
    config.update({
        'detection': {
            'confidence_threshold': 90,
            'cooldown_duration': 1.5
        }
    })
    print(f"   New confidence: {config.get('detection.confidence_threshold')}")
    print(f"   New cooldown: {config.get('detection.cooldown_duration')}")
    
    # Test save
    print("\n🧪 Test 4: Save config")
    config.save_config()
    
    # Test export
    print("\n🧪 Test 5: Export config")
    config.export_config('exported_config.json')
    
    print("\n✅ Config Manager tests completed!")