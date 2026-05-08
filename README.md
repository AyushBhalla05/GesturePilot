# GesturePilot 🚀

GesturePilot is a powerful, modular, and real-time gesture control system for your PC. It uses computer vision (OpenCV and MediaPipe) to detect hand landmarks and translate finger movements into system actions, allowing you to control your computer without touching it.

![GesturePilot Demo](gesture_pilot_hero.png)

## ✨ Key Features

- **🎯 Precision Hand Tracking**: Leverages MediaPipe for high-accuracy hand landmark detection.
- **🎨 Modern Dark Mode GUI**: Sleek and intuitive interface built with custom UI components.
- **🛠️ Action Execution**: Control system functions like Volume, Media, and more via simple hand gestures.
- **📊 Activity History**: Track all recognized gestures and executed actions in a detailed history log.
- **⚙️ Advanced Settings**: Customize detection thresholds, cooldowns, and interface preferences.
- **🔊 Voice Feedback**: Optional audio confirmation for recognized gestures.
- **🚀 Auto-Start Support**: Seamlessly integrate into your Windows startup for quick access.

## 📋 Prerequisites

Before running GesturePilot, ensure you have:
- **Python 3.8 or higher** installed.
- A functional **Webcam**.
- Windows OS (some action executors are Windows-specific).

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AyushBhalla05/GesturePilot.git
   cd GesturePilot
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

Simply run the main script to launch the application:

```bash
python main.py
```

### 🖐️ Gesture Controls

The system distinguishes between left and right hands, providing a wide range of controls:

#### ➡️ Right Hand (Primary Actions)

| Gesture | Action | Description |
|:---:|---|---|
| 👆 | **Open YouTube** | Launches YouTube in your default browser |
| ✌️ | **Play/Pause** | Toggle media playback (Music/Video) |
| 🤟 | **Volume Up** | Increase system volume |
| 🖖 | **Calculator** | Open the Windows Calculator |
| 🖐️ | **Screenshot** | Capture and save a screenshot |
| ✊ | **Stop** | Neutralize or stop the current action |
| 👍 | **Brightness Up**| Increase display brightness |

#### ⬅️ Left Hand (System & Browser)

| Gesture | Action | Description |
|:---:|---|---|
| 👆 | **New Tab** | Open a new tab in your browser (Ctrl+T) |
| ✌️ | **Close Tab** | Close the current browser tab (Ctrl+W) |
| 🤟 | **Volume Down** | Decrease system volume |
| 🖖 | **Notepad** | Open Windows Notepad for quick notes |
| 🖐️ | **Minimize All**| Show Desktop / Minimize all windows |
| ✊ | **Next Track** | Skip to the next media track |
| 👍 | **Brightness Down**| Decrease display brightness |

*(Note: These mappings can be customized in `gesture_library.json`)*


## 📂 Project Structure

To help you navigate the codebase, here is a breakdown of the key files and their responsibilities:

### 🧠 Core Logic
| File | Role |
| :--- | :--- |
| `main.py` | **The Heart of the App**: Entry point that initializes all components and runs the main loop. |
| `hand_detector.py` | **Computer Vision**: Integrates MediaPipe for real-time hand landmark detection. |
| `gesture_recognizer.py`| **Logic Layer**: Analyzes landmark data to identify specific gestures. |
| `finger_analyzer.py` | **Detailed Analysis**: Checks individual finger states (extended, folded, etc.). |
| `action_executor.py` | **The Doer**: Executes system actions like opening apps or controlling volume. |
| `system_controller.py` | **The Orchestrator**: Manages the coordination between detection and execution. |

### 🎨 User Interface
| File | Role |
| :--- | :--- |
| `ui_manager.py` | **Dashboard**: Implements the main dark-themed GUI and camera overlay. |
| `settings_panel.py` | **Customization**: GUI for adjusting sensitivity, resolution, and features. |
| `history_viewer.py` | **Visualization**: A dedicated panel to view past session logs. |

### 🛠️ Infrastructure & Utilities
| File | Role |
| :--- | :--- |
| `config_manager.py` | **Persistence**: Saves and loads user preferences from JSON files. |
| `history_manager.py` | **Data Logger**: Saves gesture history into CSV/JSON for tracking. |
| `camera_manager.py` | **Hardware**: Handles stable camera feed capture and processing. |
| `voice_feedback.py` | **Accessibility**: Provides audio confirmation for executed gestures. |
| `autostart_manager.py`| **Integration**: Manages Windows Startup settings. |

### 📁 Data & Config
- `gesture_library.json`: The source of truth for gesture-to-action mappings.
- `requirements.txt`: List of Python libraries needed to run the project.
- `screenshots/`: Visual assets showing the app in action.

---
*Note: Files like `main_phase1.py` through `main_phase4.py` represent the evolutionary stages of this project, documenting the journey from a simple detector to a full-fledged system.*


## 🛠️ Configuration

You can customize the behavior of GesturePilot by editing `exported_config.json` or using the **Settings** panel within the application:
- Adjust **Confidence Threshold** to reduce false positives.
- Change **Resolution** for better performance on older hardware.
- Toggle **Skeleton Display** and **Voice Feedback**.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new gestures or features, feel free to:
1. Fork the project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Built with ❤️ by [Ayush Bhalla](https://github.com/AyushBhalla05)
