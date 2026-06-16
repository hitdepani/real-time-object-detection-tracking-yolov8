# Installation Guide

Follow these instructions to reliably install and execute the Real-Time Object Detection and Tracking project on a fresh machine.

## 1. System Requirements
* **OS:** Windows 10/11, macOS, or Linux.
* **Hardware:** Any dual-core or quad-core CPU. No dedicated GPU is required.
* **Storage:** ~1GB free space (for Python packages and the PyTorch library).

## 2. Python Installation Instructions
Ensure you have **Python 3.10** or higher installed. 
* Download from [python.org/downloads](https://www.python.org/downloads/).
* **Crucial (Windows):** Ensure you check the box labeled **"Add Python to PATH"** during the installation process.

## 3. Virtual Environment Setup
Open your terminal (Command Prompt, PowerShell, or bash) and navigate to the extracted project folder.
```bash
python -m venv venv
```
Activate the environment:
* **Windows PowerShell:** `.\venv\Scripts\activate`
* **macOS/Linux:** `source venv/bin/activate`

## 4. Dependency Installation
With the virtual environment active (you should see `(venv)` in the terminal prompt), install the required packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Project Folder Setup
The code will automatically generate necessary folders (`outputs/`, `snapshots/`, `logs/`) upon first execution. You optionally need to create a folder to hold your test videos:
```bash
mkdir sample_videos
```
Place any `.mp4` file into this folder to test offline processing.

## 6. First-Run Instructions
Test your installation by invoking the CLI on your webcam:
```bash
python main.py --webcam
```

## 7. Download Expectations for YOLO Weights
During the very first execution, the `ultralytics` library will search for the YOLOv8n weights. If the file `yolov8n.pt` is not found in the root directory, it will automatically download it from the official GitHub releases (~6MB). You must have internet access for this initial run.

## 8. Verification Checklist
- [ ] Python version is `3.10+` (`python --version`).
- [ ] Virtual environment is activated.
- [ ] Requirements installed without errors.
- [ ] `main.py` executes successfully.
- [ ] OpenCV GUI window appears and tracks objects successfully.
