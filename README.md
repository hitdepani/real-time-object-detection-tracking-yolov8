<div align="center">

# 🎯 Real-Time Object Detection & Tracking 🚀

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8n-FF6B00?logo=ultralytics&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

**A high-performance, CPU-optimized computer vision pipeline for real-time multi-object tracking.**

[Overview](#-overview) • [Features](#-key-features) • [Demo](#-live-preview) • [Tech Stack](#-tech-stack) • [Installation](#-quick-start) • [Usage](#-usage)

<br/>
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzRzajh3Z2k2c20xdHZwdzhidGNzcGkxbWtkYWl1M20ybG8xb25yeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L1R1tvI9svkIWwpVYr/giphy.gif" width="600" alt="Object Tracking Demo GIF" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/>
<br/>
<sub><i>(Replace the placeholder above with your actual project GIF!)</i></sub>

</div>

---

## 🌟 Overview
> **For Recruiters & Evaluators:** This project demonstrates production-grade software engineering applied to computer vision. It implements a complete end-to-end pipeline that takes raw video feeds, runs them through deep learning models (**YOLOv8**), and persistently tracks entities across frames (**ByteTrack**) — all heavily optimized to run locally on a **standard CPU** without requiring expensive GPUs. 

It showcases modular design, clean separation of concerns (Detection vs. Tracking vs. I/O), graceful error handling, and robust CLI tool development.

## ✨ Key Features
- **⚡ Real-Time Processing:** Achieves fluid tracking even on low-end hardware via algorithmic frame-skipping and aggressive tensor downscaling.
- **🎯 Precision Tracking:** Utilizes the state-of-the-art **ByteTrack** algorithm to maintain identity persistence even during heavy object occlusions.
- **📸 Interactive Utilities:** Capture high-quality snapshots mid-execution or record annotated `.mp4` outputs directly to your disk.
- **💻 Zero GPU Required:** Explicitly engineered for CPU-bound environments (`device="cpu"`), democratizing advanced CV technology.
- **🛡️ Bulletproof CLI:** A professionally styled command-line interface using `argparse` with strict validation to prevent crashes.

---

## 🛠️ Tech Stack 

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12** | Core programming language |
| **Ultralytics (YOLOv8)** | Neural network architecture for instantaneous detection |
| **ByteTrack** | Double-association multi-object tracking (MOT) |
| **OpenCV** | Matrix manipulations, video I/O, and graphical overlays |
| **PyYAML** | Stateless configurations preventing hardcoded logic |

---

## 📈 Architecture & Optimizations
Why does this run so well on old laptops? 
1. **Model Selection:** Employs `yolov8n.pt` (the nano variant) which contains merely 3.2M parameters.
2. **Dynamic Downscaling:** Raw 1080p frames are crushed to a mathematical `320x320` grid, exponentially reducing matrix multiplications.
3. **Tracking by Detection:** Skips computationally heavy DeepSORT Re-ID subnetworks in favor of pure spatial geometry (Intersection over Union).
4. **Frame Skipping:** Bypasses heavy neural network loops on alternating frames, rendering the visual state from memory to save massive CPU cycles.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/hitdepani/real-time-object-detection-tracking-yolov8.git
cd real-time-object-detection-tracking-yolov8
```

### 2. Set up the environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(Note: YOLOv8 weights will automatically download on your first execution!)*

---

## 🎮 Usage

Interact with the application through the intuitive terminal interface:

**📷 Webcam Mode:**
```bash
python main.py --webcam
```

**🎬 Video File Mode:**
```bash
python main.py --video sample_videos/test.mp4
```

**💾 Save Output to Disk:**
```bash
python main.py --video sample_videos/test.mp4 --save-output
```

**🥷 Headless Mode (No GUI):**
```bash
python main.py --video sample_videos/test.mp4 --no-display
```

### ⌨️ In-App Controls
* Press <kbd>s</kbd> to capture a quick snapshot of the current frame.
* Press <kbd>q</kbd> to exit the application gracefully.

---

## 📂 Project Structure
```bash
├── main.py                # Command Line Interface (CLI) Parser
├── video_processor.py     # Central Engine: IO, Skipping, Rendering
├── detector.py            # YOLOv8 + ByteTrack PyTorch Wrapper
├── utils.py               # Moving Average FPS & File IO Helpers
├── config.py              # Configuration Gateway
├── configs/
│   └── tracking_config.yaml # Editable parameters & thresholds
└── docs/                  # Extensive academic & AI handoff documentation
```

---

<div align="center">
  <b>Built with ❤️ by Hit Depani</b><br>
  <a href="https://github.com/hitdepani">GitHub Profile</a> • <a href="mailto:your.email@example.com">Contact Me</a>
</div>
