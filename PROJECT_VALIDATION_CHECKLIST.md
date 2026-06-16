# Project Validation Checklist

This checklist is designed to verify that the project is completely ready for academic submission and live demonstration.

## Development Checklist
- [x] Code files completed (`config.py`, `utils.py`, `detector.py`, `tracker.py`, `video_processor.py`, `main.py`).
- [x] Documentation completed (`README.md`, `PROJECT_CONTEXT.md`, `TESTING_GUIDE.md`, etc.).
- [x] Configuration verified (YAML parsing functions as expected).

## Functional Checklist
- [ ] **Webcam mode works:** `python main.py --webcam` executes without crashing.
- [ ] **Video mode works:** `python main.py --video path/to/file` processes the video correctly.
- [ ] **Detection works:** Bounding boxes lock onto targets (e.g., people, cars).
- [ ] **Tracking works:** IDs persist across frames and handle minor occlusions.
- [ ] **Snapshot saving works:** Pressing `s` drops a `.jpg` in the `snapshots/` folder.
- [ ] **Output saving works:** Using `--save-output` generates a playable `.mp4` video.

## Submission Checklist
- [ ] `README.md` updated with exact system commands.
- [ ] `requirements.txt` finalized with pinned dependency versions.
- [ ] Sample video included (e.g., `test.mp4` placed in repository before zipping).
- [ ] Screenshots captured (taking snapshots of successful detections to embed in final report).

## Viva Checklist
- [ ] Can explain YOLOv8 (One-stage detection, anchor-free, regression-based).
- [ ] Can explain ByteTrack (Double-association matching, relies on IoU and Kalman Filter, not deep Re-ID).
- [ ] Can explain frame skipping (Running inference every $N$ frames to save CPU cycles).
- [ ] Can explain CPU optimizations (Downscaling image resolution, removing gradient graphs).
- [ ] Can explain project architecture (Separation of concerns between detector, tracker, and visualizer).
