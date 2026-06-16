# Real-Time Object Detection and Tracking Using YOLOv8

This project provides a robust, lightweight, CPU-optimized application for detecting and tracking objects in real-time. It leverages the Ultralytics YOLOv8 library with its built-in ByteTrack integration to offer high performance without requiring a dedicated GPU.

## Installation Instructions

1. **Prerequisites:** Ensure you have Python 3.12 installed.
2. **Virtual Environment:** 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Examples

**Webcam Mode:**
```bash
python main.py --webcam
```

**Video File Mode:**
```bash
python main.py --video sample_videos/test.mp4
```

**Save Output Video:**
```bash
python main.py --video sample_videos/test.mp4 --save-output
```

## Keyboard Shortcuts
* `q` - Quit the application cleanly.
* `s` - Save a snapshot of the current frame to the `snapshots/` directory.

## Folder Structure
```
object-detection-tracking/
├── main.py                # CLI entry point
├── detector.py            # YOLOv8 inference and tracking wrapper
├── tracker.py             # Deprecated (Tracking now internal to Ultralytics)
├── video_processor.py     # IO, looping, and visualization engine
├── utils.py               # FPS and logging utilities
├── config.py              # YAML config parser
├── configs/               
│   └── tracking_config.yaml # Detection & tracking parameters
├── requirements.txt       # Pinned dependencies
├── outputs/               # Saved annotated videos
├── snapshots/             # Saved image frames
└── logs/                  # System logs
```

## Performance Notes for Low-End Laptops
This application is strictly optimized for CPU usage:
* **Image Downscaling:** Frames are forcefully resized to `320x320` during inference.
* **Frame Skipping:** To maintain GUI responsiveness, inference can be skipped on alternating frames (adjustable via `configs/tracking_config.yaml`).
* **Built-in ByteTrack:** Avoids the heavy computational cost of deep Re-ID models (like DeepSORT) by relying purely on spatial bounding-box IoU algorithms.

## Troubleshooting Section
* **Camera Fails to Open:** Ensure no other applications (e.g., Zoom) are actively using the camera index `0`.
* **Missing Weights:** Upon the very first run, `yolov8n.pt` will automatically download from GitHub. Ensure an active internet connection.
* **Low FPS:** Increase the `skip_frames` parameter in `configs/tracking_config.yaml` to `2` or `3`.

