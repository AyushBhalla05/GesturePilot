# GesturePilot 🚀

GesturePilot is a powerful, modular, and real-time gesture control system for your PC. It uses computer vision (OpenCV and MediaPipe) to detect hand landmarks and translate finger movements into system actions, allowing you to control your computer without touching it.

![GesturePilot Demo](screenshot_20260509_004019.png)

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

### 🖐️ Basic Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| 🖐️ Open Palm | None | Neutral state |
| ☝️ Index Up | Move Mouse | Control cursor |
| ✌️ V-Sign | Volume Up | Increase system volume |
| 🤙 Call Sign | Volume Down | Decrease system volume |
| ✊ Fist | Mute | Toggle system mute |

*(Note: Gestures can be customized in `gesture_library.json`)*

## 📂 Project Structure

```text
GesturePilot/
├── main.py                # Entry point
├── hand_detector.py       # MediaPipe integration
├── gesture_recognizer.py  # Gesture logic
├── action_executor.py     # System control logic
├── ui_manager.py          # GUI implementation
├── settings_panel.py      # Configuration interface
├── history_manager.py     # Data logging
├── config_manager.py      # Settings management
└── requirements.txt       # Dependencies
```

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
