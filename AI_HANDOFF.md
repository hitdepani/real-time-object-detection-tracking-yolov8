# AI Handoff Document

This file provides crucial context for future AI assistants (Codex, Cursor, Claude, ChatGPT, Antigravity) to seamlessly resume development or refactor this codebase.

## 1. Project Purpose
A real-time, CPU-optimized object detection and tracking pipeline. Built for academic demonstration, prioritizing code readability, error handling, and hardware inclusivity over raw GPU throughput.

## 2. Folder Structure Overview
*   **main.py**: CLI parser (`argparse`).
*   **video_processor.py**: Main execution loop (IO, rendering, frame skipping).
*   **detector.py**: Core ML logic, utilizing `ultralytics` for inference and tracking.
*   **tracker.py**: Deprecated.
*   **utils.py**: Helpers (FPS, logging).

## 3. File Responsibility Summary
*   `config.py` parses YAML files statically to avoid runtime overhead.
*   `detector.py` uses `YOLO.track(persist=True)` to offload Kalman filtering and Hungarian matching to the natively optimized C++/Python libraries within Ultralytics.
*   `video_processor.py` strictly manages the OpenCV visualization layer.

## 4. Architectural Principles
*   **Robustness:** Main application loops are heavily wrapped in `try/except` blocks. If tracking fails on a frame, it skips processing rather than crashing the system.
*   **CPU Optimization:** `imgsz` is hardcoded down to 320 to maintain high FPS on legacy hardware. `skip_frames` allows decoupling the render loop from the heavy inference loop.

## 5. Extension Guidelines
To add new features (e.g., counting cars crossing a line), inject the geometric line-intersection logic directly into `video_processor.py::_draw_results()` utilizing the `last_tracks` list.

## 6. Known Limitations
*   ByteTrack relies purely on spatial bounding-box IoU. Deep-learning appearance extraction (Re-ID) is intentionally disabled to save CPU cycles. Track IDs will swap during heavy occlusion.

## 7. Safe Modification Practices
*   Do not re-introduce manual tracker libraries (like `norfair` or standalone `byte_tracker`). The Ultralytics internal tracker handles model state via the `persist=True` flag perfectly.

## 8. Recommended Order for Reviewing Files
1. `config.py` -> 2. `detector.py` -> 3. `video_processor.py` -> 4. `main.py`.

## 9. Important Assumptions
*   Python 3.12 is used. 
*   Internet is available on the first run to fetch `yolov8n.pt`.

## 10. Future Enhancement Ideas
*   Threaded video ingestion to unblock the main loop.
*   Web interface using Flask (if the CPU overhead of serving HTTP allows it).
