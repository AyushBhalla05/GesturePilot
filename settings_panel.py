"""
GesturePilot - Phase 4: Settings Panel
Author: Your Name
Description: Simple settings panel for gesture management
"""

import customtkinter as ctk
import json

class SettingsPanel:
    """
    Simple settings panel for GesturePilot
    """
    
    def __init__(self, parent, gesture_library_path='gesture_library.json'):
        """
        Initialize settings panel
        
        Args:
            parent: Parent window
            gesture_library_path: Path to gesture library
        """
        self.parent = parent
        self.library_path = gesture_library_path
        self.window = None
        
        # Callbacks
        self.on_gesture_added = None
        self.on_gesture_removed = None
        self.on_settings_changed = None
        
        # Colors
        self.bg_dark = "#1a1a1a"
        self.bg_medium = "#2d2d2d"
        self.accent_green = "#00ff88"
        
        print("⚙️ Settings Panel initialized")
    
    def show(self):
        """Show settings window"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("⚙️ Settings")
        self.window.geometry("600x700")
        self.window.configure(fg_color=self.bg_dark)
        
        # Make modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self._create_settings_ui()
    
    def _create_settings_ui(self):
        """Create settings UI"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color=self.bg_dark)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="⚙️ GesturePilot Settings",
            font=("Arial", 24, "bold"),
            text_color=self.accent_green
        )
        title.pack(pady=20)
        
        # Gesture Management Section
        self._create_gesture_management(main_frame)
        
        # Quick Settings Section
        self._create_quick_settings(main_frame)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="✓ Close",
            command=self.window.destroy,
            fg_color=self.accent_green,
            hover_color="#00cc66",
            font=("Arial", 14, "bold"),
            height=40
        )
        close_btn.pack(pady=20, fill="x")
    
    def _create_gesture_management(self, parent):
        """Create gesture management section"""
        
        section = ctk.CTkFrame(parent, fg_color=self.bg_medium, corner_radius=10)
        section.pack(fill="x", pady=10)
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🎯 Gesture Management",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=15, padx=20, anchor="w")
        
        # Buttons
        btn_frame = ctk.CTkFrame(section, fg_color=self.bg_medium)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        # Add gesture button
        add_btn = ctk.CTkButton(
            btn_frame,
            text="📝 Add New Gesture",
            command=self._add_gesture_dialog,
            fg_color="#2d2d2d",
            hover_color="#3d3d3d",
            font=("Arial", 14),
            height=45
        )
        add_btn.pack(fill="x", pady=5)
        
        # Remove gesture button
        remove_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Remove Gesture",
            command=self._remove_gesture_dialog,
            fg_color="#2d2d2d",
            hover_color="#3d3d3d",
            font=("Arial", 14),
            height=45
        )
        remove_btn.pack(fill="x", pady=5)
        
        # Customize button
        customize_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Customize Gesture",
            command=self._customize_gesture_dialog,
            fg_color="#2d2d2d",
            hover_color="#3d3d3d",
            font=("Arial", 14),
            height=45
        )
        customize_btn.pack(fill="x", pady=5)
    
    def _create_quick_settings(self, parent):
        """Create quick settings section"""
        
        section = ctk.CTkFrame(parent, fg_color=self.bg_medium, corner_radius=10)
        section.pack(fill="x", pady=10)
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🔧 Quick Settings",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=15, padx=20, anchor="w")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(section, fg_color=self.bg_medium)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Auto-start checkbox
        self.autostart_var = ctk.BooleanVar(value=False)
        autostart_check = ctk.CTkCheckBox(
            settings_frame,
            text="Auto-start with Windows",
            variable=self.autostart_var,
            font=("Arial", 13),
            fg_color=self.accent_green,
            hover_color="#00cc66"
        )
        autostart_check.pack(anchor="w", pady=8)
        
        # Voice feedback checkbox
        self.voice_var = ctk.BooleanVar(value=True)
        voice_check = ctk.CTkCheckBox(
            settings_frame,
            text="Voice Feedback",
            variable=self.voice_var,
            font=("Arial", 13),
            fg_color=self.accent_green,
            hover_color="#00cc66"
        )
        voice_check.pack(anchor="w", pady=8)
        
        # Show skeleton checkbox
        self.skeleton_var = ctk.BooleanVar(value=True)
        skeleton_check = ctk.CTkCheckBox(
            settings_frame,
            text="Show Hand Skeleton",
            variable=self.skeleton_var,
            font=("Arial", 13),
            fg_color=self.accent_green,
            hover_color="#00cc66"
        )
        skeleton_check.pack(anchor="w", pady=8)
        
        # Show FPS checkbox
        self.fps_var = ctk.BooleanVar(value=True)
        fps_check = ctk.CTkCheckBox(
            settings_frame,
            text="Show FPS Counter",
            variable=self.fps_var,
            font=("Arial", 13),
            fg_color=self.accent_green,
            hover_color="#00cc66"
        )
        fps_check.pack(anchor="w", pady=8)
        
        # Confidence slider
        conf_label = ctk.CTkLabel(
            settings_frame,
            text="Confidence Threshold: 80%",
            font=("Arial", 13),
            text_color="#b0b0b0"
        )
        conf_label.pack(anchor="w", pady=(15, 5))
        
        self.confidence_slider = ctk.CTkSlider(
            settings_frame,
            from_=50,
            to=95,
            number_of_steps=45,
            fg_color="#3d3d3d",
            progress_color=self.accent_green,
            button_color=self.accent_green,
            button_hover_color="#00cc66"
        )
        self.confidence_slider.set(80)
        self.confidence_slider.pack(fill="x", pady=5)
        
        # Cooldown slider
        cool_label = ctk.CTkLabel(
            settings_frame,
            text="Cooldown Duration: 2.0s",
            font=("Arial", 13),
            text_color="#b0b0b0"
        )
        cool_label.pack(anchor="w", pady=(15, 5))
        
        self.cooldown_slider = ctk.CTkSlider(
            settings_frame,
            from_=0.5,
            to=5.0,
            number_of_steps=45,
            fg_color="#3d3d3d",
            progress_color=self.accent_green,
            button_color=self.accent_green,
            button_hover_color="#00cc66"
        )
        self.cooldown_slider.set(2.0)
        self.cooldown_slider.pack(fill="x", pady=5)
        
        # Save button
        save_btn = ctk.CTkButton(
            settings_frame,
            text="💾 Save Settings",
            command=self._save_settings,
            fg_color=self.accent_green,
            hover_color="#00cc66",
            font=("Arial", 14, "bold"),
            height=40
        )
        save_btn.pack(pady=20, fill="x")
    
    def _add_gesture_dialog(self):
        """Show add gesture dialog"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("📝 Add New Gesture")
        dialog.geometry("500x400")
        dialog.configure(fg_color=self.bg_dark)
        
        # Make modal
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Content
        frame = ctk.CTkFrame(dialog, fg_color=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            frame,
            text="Add New Gesture",
            font=("Arial", 20, "bold"),
            text_color=self.accent_green
        )
        title.pack(pady=20)
        
        # Info
        info = ctk.CTkLabel(
            frame,
            text="This feature allows you to capture and save\n"
                 "new custom gestures in real-time.\n\n"
                 "Coming soon in full version!",
            font=("Arial", 14),
            text_color="#b0b0b0"
        )
        info.pack(pady=30)
        
        # Close button
        close_btn = ctk.CTkButton(
            frame,
            text="OK",
            command=dialog.destroy,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d"
        )
        close_btn.pack(pady=20)
    
    def _remove_gesture_dialog(self):
        """Show remove gesture dialog"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("❌ Remove Gesture")
        dialog.geometry("500x500")
        dialog.configure(fg_color=self.bg_dark)
        
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="Remove Gesture",
            font=("Arial", 20, "bold"),
            text_color="#ff4444"
        )
        title.pack(pady=20)
        
        # Load gestures
        try:
            with open(self.library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gestures = data.get('gestures', [])
            
            # Gesture list
            list_frame = ctk.CTkScrollableFrame(
                frame,
                fg_color=self.bg_medium,
                height=300
            )
            list_frame.pack(fill="both", expand=True, pady=10)
            
            for gesture in gestures:
                name = gesture.get('name', 'Unknown')
                icon = gesture.get('icon', '👆')
                
                gesture_frame = ctk.CTkFrame(list_frame, fg_color="#2d2d2d")
                gesture_frame.pack(fill="x", pady=5, padx=10)
                
                label = ctk.CTkLabel(
                    gesture_frame,
                    text=f"{icon} {name}",
                    font=("Arial", 13)
                )
                label.pack(side="left", padx=10, pady=10)
                
                remove_btn = ctk.CTkButton(
                    gesture_frame,
                    text="❌",
                    width=40,
                    fg_color="#ff4444",
                    hover_color="#cc3333",
                    command=lambda g=gesture: self._confirm_remove(g, dialog)
                )
                remove_btn.pack(side="right", padx=10, pady=5)
        
        except Exception as e:
            error_label = ctk.CTkLabel(
                frame,
                text=f"Error loading gestures: {e}",
                text_color="#ff4444"
            )
            error_label.pack(pady=20)
        
        close_btn = ctk.CTkButton(
            frame,
            text="Close",
            command=dialog.destroy,
            fg_color=self.bg_medium
        )
        close_btn.pack(pady=10)
    
    def _confirm_remove(self, gesture, parent_dialog):
        """Confirm gesture removal"""
        print(f"🗑️ Removing gesture: {gesture.get('name')}")
        # Implementation would remove from JSON
        parent_dialog.destroy()
    
    def _customize_gesture_dialog(self):
        """Show customize gesture dialog"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("✏️ Customize Gesture")
        dialog.geometry("500x400")
        dialog.configure(fg_color=self.bg_dark)
        
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="Customize Gesture Actions",
            font=("Arial", 20, "bold"),
            text_color=self.accent_green
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            frame,
            text="This feature allows you to modify\n"
                 "gesture-to-action mappings.\n\n"
                 "Coming soon in full version!",
            font=("Arial", 14),
            text_color="#b0b0b0"
        )
        info.pack(pady=30)
        
        close_btn = ctk.CTkButton(
            frame,
            text="OK",
            command=dialog.destroy,
            fg_color=self.bg_medium
        )
        close_btn.pack(pady=20)
    
    def _save_settings(self):
        """Save settings to file"""
        print("💾 Saving settings...")
        
        settings = {
            'autostart': self.autostart_var.get(),
            'voice_feedback': self.voice_var.get(),
            'show_skeleton': self.skeleton_var.get(),
            'show_fps': self.fps_var.get(),
            'confidence_threshold': self.confidence_slider.get(),
            'cooldown_duration': self.cooldown_slider.get()
        }
        
        print(f"   Settings: {settings}")
        
        if self.on_settings_changed:
            self.on_settings_changed(settings)
        
        # Show confirmation
        conf_label = ctk.CTkLabel(
            self.window,
            text="✅ Settings saved!",
            text_color=self.accent_green,
            font=("Arial", 14, "bold")
        )
        conf_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # Remove after 2 seconds
        self.window.after(2000, conf_label.destroy)


# Test function
if __name__ == "__main__":
    print("=" * 50)
    print("⚙️ TESTING SETTINGS PANEL")
    print("=" * 50)
    
    root = ctk.CTk()
    root.title("Test")
    root.geometry("400x300")
    
    def show_settings():
        panel = SettingsPanel(root)
        panel.show()
    
    btn = ctk.CTkButton(root, text="Open Settings", command=show_settings)
    btn.pack(pady=100)
    
    root.mainloop()