"""
GesturePilot - Phase 4: UI Manager
Author: Your Name
Description: Dark mode GUI using CustomTkinter
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading

class UIManager:
    """
    Manages the dark mode GUI for GesturePilot
    """
    
    def __init__(self, title="GesturePilot", width=1200, height=800):
        """
        Initialize UI Manager
        
        Args:
            title (str): Window title
            width (int): Window width
            height (int): Window height
        """
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        
        # Colors
        self.bg_dark = "#1a1a1a"
        self.bg_medium = "#2d2d2d"
        self.accent_green = "#00ff88"
        self.text_light = "#ffffff"
        self.text_gray = "#b0b0b0"
        
        # State
        self.is_running = False
        self.current_frame = None
        self.video_update_thread = None
        
        # Callbacks
        self.on_settings_click = None
        self.on_history_click = None
        self.on_stop_click = None
        self.on_pause_click = None
        
        print("🎨 UI Manager initialized (Dark Mode)")
        
        self._create_ui()
    
    def _create_ui(self):
        """Create main UI elements"""
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.bg_dark)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Top status bar
        self._create_status_bar()
        
        # Camera feed area
        self._create_camera_area()
        
        # Info panel
        self._create_info_panel()
        
        # Control buttons
        self._create_control_buttons()
    
    def _create_status_bar(self):
        """Create status bar at top"""
        status_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_medium,
            corner_radius=10
        )
        status_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        status_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # FPS label
        self.fps_label = ctk.CTkLabel(
            status_frame,
            text="FPS: --",
            text_color=self.accent_green,
            font=("Arial", 16, "bold")
        )
        self.fps_label.grid(row=0, column=0, padx=20, pady=10)
        
        # Person status
        self.person_label = ctk.CTkLabel(
            status_frame,
            text="Person: --",
            text_color=self.text_gray,
            font=("Arial", 14)
        )
        self.person_label.grid(row=0, column=1, padx=20, pady=10)
        
        # Hands count
        self.hands_label = ctk.CTkLabel(
            status_frame,
            text="Hands: 0",
            text_color=self.text_gray,
            font=("Arial", 14)
        )
        self.hands_label.grid(row=0, column=2, padx=20, pady=10)
        
        # Voice status
        self.voice_label = ctk.CTkLabel(
            status_frame,
            text="🔊 Voice: ON",
            text_color=self.accent_green,
            font=("Arial", 14)
        )
        self.voice_label.grid(row=0, column=3, padx=20, pady=10)
    
    def _create_camera_area(self):
        """Create camera feed display area"""
        camera_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#000000",
            corner_radius=10
        )
        camera_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Canvas for video
        self.camera_label = ctk.CTkLabel(
            camera_frame,
            text="📹 Camera Initializing...",
            text_color=self.text_gray,
            font=("Arial", 20)
        )
        self.camera_label.pack(expand=True, fill="both", padx=10, pady=10)
    
    def _create_info_panel(self):
        """Create info panel below camera"""
        info_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_medium,
            corner_radius=10,
            height=120
        )
        info_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Last gesture
        self.gesture_label = ctk.CTkLabel(
            info_frame,
            text="🎯 Last Gesture: None",
            text_color=self.text_light,
            font=("Arial", 14)
        )
        self.gesture_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Last action
        self.action_label = ctk.CTkLabel(
            info_frame,
            text="⚡ Last Action: None",
            text_color=self.text_gray,
            font=("Arial", 12)
        )
        self.action_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        # Confidence
        self.confidence_label = ctk.CTkLabel(
            info_frame,
            text="Confidence: --%",
            text_color=self.text_gray,
            font=("Arial", 12)
        )
        self.confidence_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    
    def _create_control_buttons(self):
        """Create control buttons at bottom"""
        button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_dark
        )
        button_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ Settings",
            command=self._on_settings,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d",
            font=("Arial", 14)
        )
        self.settings_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # History button
        self.history_btn = ctk.CTkButton(
            button_frame,
            text="📊 History",
            command=self._on_history,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d",
            font=("Arial", 14)
        )
        self.history_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Pause button
        self.pause_btn = ctk.CTkButton(
            button_frame,
            text="⏸️ Pause",
            command=self._on_pause,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d",
            font=("Arial", 14)
        )
        self.pause_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="🛑 Stop",
            command=self._on_stop,
            fg_color="#ff4444",
            hover_color="#cc3333",
            font=("Arial", 14, "bold")
        )
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    
    # ========== UPDATE METHODS ==========
    
    def update_fps(self, fps):
        """Update FPS display"""
        color = self.accent_green if fps > 25 else "#ffaa00"
        self.fps_label.configure(text=f"FPS: {int(fps)}", text_color=color)
    
    def update_person_status(self, detected, message=""):
        """Update person detection status"""
        color = self.accent_green if detected else "#ff4444"
        text = f"Person: {'✓' if detected else '✗'}"
        if message:
            text = f"Person: {message}"
        self.person_label.configure(text=text, text_color=color)
    
    def update_hands_count(self, count):
        """Update hands count"""
        color = self.accent_green if count > 0 else self.text_gray
        self.hands_label.configure(text=f"Hands: {count}", text_color=color)
    
    def update_voice_status(self, enabled):
        """Update voice feedback status"""
        text = "🔊 Voice: ON" if enabled else "🔇 Voice: OFF"
        color = self.accent_green if enabled else self.text_gray
        self.voice_label.configure(text=text, text_color=color)
    
    def update_gesture_info(self, gesture_name=None, action=None, confidence=None):
        """Update gesture information"""
        if gesture_name:
            self.gesture_label.configure(text=f"🎯 Last Gesture: {gesture_name}")
        
        if action:
            self.action_label.configure(text=f"⚡ Last Action: {action}")
        
        if confidence is not None:
            color = self.accent_green if confidence > 80 else "#ffaa00"
            self.confidence_label.configure(
                text=f"Confidence: {confidence:.0f}%",
                text_color=color
            )
    
    def update_camera_frame(self, frame_bgr):
        """
        Update camera display with new frame
        
        Args:
            frame_bgr: OpenCV frame in BGR format
        """
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            
            # Resize to fit display (maintain aspect ratio)
            display_width = 1180
            display_height = 600
            
            h, w = frame_rgb.shape[:2]
            aspect = w / h
            
            if aspect > display_width / display_height:
                new_w = display_width
                new_h = int(display_width / aspect)
            else:
                new_h = display_height
                new_w = int(display_height * aspect)
            
            frame_resized = cv2.resize(frame_rgb, (new_w, new_h))
            
            # Convert to PhotoImage
            img = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image=img)
            
            # Update label
            self.camera_label.configure(image=photo, text="")
            self.camera_label.image = photo  # Keep reference
            
        except Exception as e:
            print(f"⚠️ Frame update error: {e}")
    
    # ========== BUTTON CALLBACKS ==========
    
    def _on_settings(self):
        """Settings button clicked"""
        if self.on_settings_click:
            self.on_settings_click()
    
    def _on_history(self):
        """History button clicked"""
        if self.on_history_click:
            self.on_history_click()
    
    def _on_pause(self):
        """Pause button clicked"""
        if self.on_pause_click:
            is_paused = self.on_pause_click()
            if is_paused:
                self.pause_btn.configure(text="▶️ Resume")
            else:
                self.pause_btn.configure(text="⏸️ Pause")
    
    def _on_stop(self):
        """Stop button clicked"""
        if self.on_stop_click:
            self.on_stop_click()
        self.root.quit()
    
    # ========== WINDOW MANAGEMENT ==========
    
    def start(self):
        """Start the UI main loop"""
        print("🎨 Starting UI...")
        self.is_running = True
        self.root.mainloop()
    
    def stop(self):
        """Stop the UI"""
        self.is_running = False
        self.root.quit()
    
    def get_root(self):
        """Get root window"""
        return self.root


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("🎨 TESTING UI MANAGER")
    print("=" * 50)
    
    ui = UIManager(title="GesturePilot - UI Test")
    
    # Test updates
    ui.update_fps(30)
    ui.update_person_status(True, "Single person")
    ui.update_hands_count(2)
    ui.update_voice_status(True)
    ui.update_gesture_info("One Finger (Right)", "open_youtube", 85.5)
    
    print("\n✅ UI initialized! Window should appear.")
    print("   Close window to exit test")
    
    ui.start()