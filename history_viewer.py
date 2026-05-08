"""
GesturePilot - Phase 5: History Viewer
Author: Your Name
Description: GUI for viewing gesture history
"""

import customtkinter as ctk
from datetime import datetime

class HistoryViewer:
    """
    GUI window for viewing gesture history
    """
    
    def __init__(self, parent, history_manager):
        """
        Initialize history viewer
        
        Args:
            parent: Parent window
            history_manager: HistoryManager instance
        """
        self.parent = parent
        self.history_manager = history_manager
        self.window = None
        
        # Colors
        self.bg_dark = "#1a1a1a"
        self.bg_medium = "#2d2d2d"
        self.accent_green = "#00ff88"
        self.text_light = "#ffffff"
        self.text_gray = "#b0b0b0"
        
        print("📊 History Viewer initialized")
    
    def show(self):
        """Show history window"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("📊 Gesture History")
        self.window.geometry("900x700")
        self.window.configure(fg_color=self.bg_dark)
        
        # Make modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self._create_ui()
        self._load_history()
    
    def _create_ui(self):
        """Create history UI"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color=self.bg_dark)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="📊 Gesture History",
            font=("Arial", 24, "bold"),
            text_color=self.accent_green
        )
        title.pack(pady=(0, 20))
        
        # Statistics section
        self._create_statistics_section(main_frame)
        
        # History table
        self._create_history_table(main_frame)
        
        # Action buttons
        self._create_action_buttons(main_frame)
    
    def _create_statistics_section(self, parent):
        """Create statistics display"""
        
        stats_frame = ctk.CTkFrame(parent, fg_color=self.bg_medium, corner_radius=10)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title = ctk.CTkLabel(
            stats_frame,
            text="📈 Statistics",
            font=("Arial", 18, "bold"),
            text_color=self.text_light
        )
        title.pack(pady=15, padx=20, anchor="w")
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame, fg_color=self.bg_medium)
        stats_grid.pack(fill="x", padx=20, pady=(0, 15))
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Get statistics
        stats = self.history_manager.get_statistics()
        
        # Total actions
        self._create_stat_card(stats_grid, "Total Actions", 
                               str(stats['total']), 0)
        
        # Success rate
        self._create_stat_card(stats_grid, "Success Rate", 
                               f"{stats['success_rate']:.1f}%", 1)
        
        # Most used gesture
        self._create_stat_card(stats_grid, "Most Used Gesture", 
                               stats['most_used_gesture'], 2)
        
        # Most used action
        self._create_stat_card(stats_grid, "Most Used Action", 
                               stats['most_used_action'][:15] + "...", 3)
    
    def _create_stat_card(self, parent, label, value, column):
        """Create a stat card"""
        
        card = ctk.CTkFrame(parent, fg_color="#2d2d2d")
        card.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 11),
            text_color=self.text_gray
        )
        label_widget.pack(pady=(10, 5))
        
        value_widget = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            text_color=self.accent_green
        )
        value_widget.pack(pady=(0, 10))
    
    def _create_history_table(self, parent):
        """Create scrollable history table"""
        
        table_frame = ctk.CTkFrame(parent, fg_color=self.bg_medium, corner_radius=10)
        table_frame.pack(fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(
            table_frame,
            text="📋 Recent Actions (Last 100)",
            font=("Arial", 18, "bold"),
            text_color=self.text_light
        )
        title.pack(pady=15, padx=20, anchor="w")
        
        # Header
        header_frame = ctk.CTkFrame(table_frame, fg_color="#2d2d2d")
        header_frame.pack(fill="x", padx=20, pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        headers = ["#", "Time", "Gesture", "Action", "Hand", "Status"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color=self.text_gray
            )
            label.grid(row=0, column=i, padx=5, pady=10)
        
        # Scrollable content
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_frame,
            fg_color=self.bg_dark,
            height=300
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    
    def _load_history(self):
        """Load and display history entries"""
        
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Get history
        history = self.history_manager.get_history()
        
        if not history:
            no_data = ctk.CTkLabel(
                self.scroll_frame,
                text="No history data available",
                font=("Arial", 14),
                text_color=self.text_gray
            )
            no_data.grid(row=0, column=0, columnspan=6, pady=50)
            return
        
        # Display entries (most recent first)
        for idx, entry in enumerate(reversed(history)):
            row = idx
            
            # Row background
            row_color = "#2d2d2d" if idx % 2 == 0 else self.bg_dark
            
            # ID
            id_label = ctk.CTkLabel(
                self.scroll_frame,
                text=str(entry['id']),
                font=("Arial", 11),
                fg_color=row_color
            )
            id_label.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
            
            # Time
            time_str = entry['datetime_readable'].split(' ')[1]  # Just time
            time_label = ctk.CTkLabel(
                self.scroll_frame,
                text=time_str,
                font=("Arial", 11),
                fg_color=row_color
            )
            time_label.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            
            # Gesture
            gesture_label = ctk.CTkLabel(
                self.scroll_frame,
                text=entry['gesture'][:20],
                font=("Arial", 11),
                fg_color=row_color
            )
            gesture_label.grid(row=row, column=2, padx=5, pady=5, sticky="ew")
            
            # Action
            action_label = ctk.CTkLabel(
                self.scroll_frame,
                text=entry['action'].replace('_', ' ')[:15],
                font=("Arial", 11),
                fg_color=row_color
            )
            action_label.grid(row=row, column=3, padx=5, pady=5, sticky="ew")
            
            # Hand
            hand_color = "#0066ff" if entry['hand'].lower() == 'right' else "#ff6600"
            hand_label = ctk.CTkLabel(
                self.scroll_frame,
                text=entry['hand'].upper(),
                font=("Arial", 11, "bold"),
                text_color=hand_color,
                fg_color=row_color
            )
            hand_label.grid(row=row, column=4, padx=5, pady=5, sticky="ew")
            
            # Status
            status_icon = "✅" if entry['status'] == 'success' else "❌"
            status_color = self.accent_green if entry['status'] == 'success' else "#ff4444"
            status_label = ctk.CTkLabel(
                self.scroll_frame,
                text=status_icon,
                font=("Arial", 14),
                text_color=status_color,
                fg_color=row_color
            )
            status_label.grid(row=row, column=5, padx=5, pady=5, sticky="ew")
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        
        button_frame = ctk.CTkFrame(parent, fg_color=self.bg_dark)
        button_frame.pack(fill="x", pady=(15, 0))
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self._refresh,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d",
            font=("Arial", 13)
        )
        refresh_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Export button
        export_btn = ctk.CTkButton(
            button_frame,
            text="📥 Export CSV",
            command=self._export,
            fg_color=self.bg_medium,
            hover_color="#3d3d3d",
            font=("Arial", 13)
        )
        export_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Clear button
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear All",
            command=self._clear,
            fg_color="#ff4444",
            hover_color="#cc3333",
            font=("Arial", 13)
        )
        clear_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="✓ Close",
            command=self.window.destroy,
            fg_color=self.accent_green,
            hover_color="#00cc66",
            font=("Arial", 13, "bold")
        )
        close_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    
    def _refresh(self):
        """Refresh history display"""
        print("🔄 Refreshing history...")
        self._load_history()
        self._update_statistics()
    
    def _export(self):
        """Export history to CSV"""
        print("📥 Exporting history...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gesture_history_{timestamp}.csv"
        
        success = self.history_manager.export_to_csv(filename)
        
        if success:
            # Show confirmation
            msg = ctk.CTkLabel(
                self.window,
                text=f"✅ Exported to {filename}",
                text_color=self.accent_green,
                font=("Arial", 13, "bold")
            )
            msg.place(relx=0.5, rely=0.95, anchor="center")
            self.window.after(3000, msg.destroy)
    
    def _clear(self):
        """Clear all history"""
        # Confirmation dialog
        confirm = ctk.CTkToplevel(self.window)
        confirm.title("⚠️ Confirm")
        confirm.geometry("400x200")
        confirm.configure(fg_color=self.bg_dark)
        confirm.transient(self.window)
        confirm.grab_set()
        
        frame = ctk.CTkFrame(confirm, fg_color=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(
            frame,
            text="⚠️ Clear All History?\n\nThis action cannot be undone!",
            font=("Arial", 16),
            text_color=self.text_light
        )
        label.pack(pady=30)
        
        btn_frame = ctk.CTkFrame(frame, fg_color=self.bg_dark)
        btn_frame.pack(fill="x", pady=10)
        
        def do_clear():
            self.history_manager.clear_history()
            self._refresh()
            confirm.destroy()
        
        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Yes, Clear",
            command=do_clear,
            fg_color="#ff4444",
            hover_color="#cc3333",
            width=150
        )
        yes_btn.pack(side="left", padx=5)
        
        no_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=confirm.destroy,
            fg_color=self.bg_medium,
            width=150
        )
        no_btn.pack(side="right", padx=5)
    
    def _update_statistics(self):
        """Update statistics display"""
        # Would need to recreate stats section
        # For simplicity, full refresh on stats change
        pass


# Test function
if __name__ == "__main__":
    from history_manager import HistoryManager
    
    print("=" * 50)
    print("📊 TESTING HISTORY VIEWER")
    print("=" * 50)
    
    # Create history with test data
    history = HistoryManager(max_size=20)
    
    # Add test data
    for i in range(15):
        history.add_action(
            f"Gesture {i % 5}",
            f"action_{i % 3}",
            "right" if i % 2 == 0 else "left",
            80 + (i % 20),
            "success" if i % 4 != 0 else "failed"
        )
    
    # Create GUI
    root = ctk.CTk()
    root.title("Test")
    root.geometry("400x300")
    
    def show_history():
        viewer = HistoryViewer(root, history)
        viewer.show()
    
    btn = ctk.CTkButton(root, text="Open History", command=show_history)
    btn.pack(pady=100)
    
    root.mainloop()