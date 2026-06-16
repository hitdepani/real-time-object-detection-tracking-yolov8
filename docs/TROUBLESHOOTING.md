# docs/TROUBLESHOOTING.md - System Troubleshooting Guide

This guide details common error states, performance bottlenecks, and resolution procedures for the YOLOv8 and ByteTrack Object Tracking system.

---

## 1. Installation and Environment Errors

### Error: `ModuleNotFoundError: No module named 'ultralytics'`
*   **Cause**: The virtual environment is either not activated or the packages were not installed.
*   **Solution**:
    1.  Verify the virtual environment is activated (you should see `(venv)` in your terminal prompt).
    2.  Run installation:
        ```bash
        pip install -r requirements.txt
        ```

### Error: `ImportError: libGL.so.1: cannot open shared object file` (Linux Environments)
*   **Cause**: Missing OpenGL libraries required by OpenCV.
*   **Solution**:
    Install OpenGL dependencies on your system:
    ```bash
    sudo apt-get update
    sudo apt-get install -y libgl1-mesa-glx
    ```

---

## 2. Ingestion and Camera Failures

### Issue: Program hangs or fails to open Webcam (`source 0`)
*   **Cause**: 
    1.  The camera is in use by another program (e.g. Teams, Zoom, Browser).
    2.  The webcam index is incorrect (e.g., external webcam is index `1`).
*   **Solution**:
    1.  Close all applications using the camera.
    2.  Query available camera indexes by changing `--source 0` to `--source 1` or `--source 2`.
    3.  Check system privacy settings to ensure Python has permission to access the camera.

### Issue: `cv2.error: OpenCV(4.x.x) ... error: (-215:Assertion failed) !ssize.empty()`
*   **Cause**: The system attempted to process a frame, but the frame was empty (e.g., end of video file, or camera disconnected).
*   **Solution**:
    *   Verify the path to the video file is correct: `--source data/input/my_video.mp4`.
    *   Ensure the video file is not corrupt.

---

## 3. Performance Bottlenecks (Low FPS)

### Symptom: Processing is slow (FPS < 5) on older laptop CPUs
*   **Cause**: 
    1.  Inference resolution is set too high (default `640x640`).
    2.  Frame skipping is disabled.
    3.  OpenCV visual rendering is bottlenecking the main loop.
*   **Solution**:
    1.  **Reduce Image Size**: Run the pipeline with `--imgsz 320`.
    2.  **Enable Frame Skipping**: Run with `--skip-frames 2` or `--skip-frames 3` to run detection on every 2nd or 3rd frame.
    3.  **Headless Execution**: Use the `--no-display` flag if running in a background environment.
    4.  **Processors Config**: Set PyTorch threads limit. Run this command in terminal before launching the program to restrict core overhead:
        ```bash
        # Windows PowerShell
        $env:OMP_NUM_THREADS="2"
        $env:MKL_NUM_THREADS="2"
        ```

---

## 4. Tracking Quality Failures (Frequent ID Switches)

### Issue: Targets switch IDs frequently when crossing paths or passing behind poles
*   **Cause**: 
    1.  High-confidence threshold is too restrictive, filtering targets too early.
    2.  The `track_buffer` parameter is too low, discarding tracks as soon as they are occluded for a few frames.
*   **Solution**:
    1.  Adjust the config inside `configs/tracking_config.yaml`:
        *   Increase `track_buffer` (e.g., from 30 frames to 60 frames) to keep lost tracks active longer.
        *   Lower `conf_threshold` slightly (e.g., from 0.25 to 0.20) to detect objects in low lighting.
        *   Modify `match_thresh` (IoU threshold) to adjust how close matches must be to pair.
