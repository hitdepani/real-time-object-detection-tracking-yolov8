# Project Architecture and Context

**Project Title:** Real-Time Object Detection and Tracking Using YOLOv8
**Phase:** Finalized

## Architecture Overview
The system employs a flattened modular architecture optimized for low-end CPU hardware. 

* **main.py**: Handles user CLI interactions and bootstraps the video pipeline.
* **video_processor.py**: The central engine. It continuously reads video frames, manages frame-skipping optimizations, applies bounding box annotations, tracks FPS using a moving average, and writes the output back to the disk or screen.
* **detector.py**: Houses the `ObjectDetector` class. It loads the `yolov8n.pt` weights and exposes a `track()` method. It leverages the internal Ultralytics `model.track(persist=True)` API to run YOLOv8 object detection paired with ByteTrack identity associations entirely within PyTorch.
* **tracker.py**: Deprecated. Previous iterations manually attempted to bridge YOLO detections with external ByteTrack modules. This proved unstable across API updates and is now deprecated in favor of Ultralytics' built-in pipeline.
* **utils.py**: Stateless helper functions for logging, directory creation, frame saving, and FPS computation.
* **config.py**: Parses `configs/tracking_config.yaml` to supply global thresholds (IoU, confidence, tracking buffers).

## Design Constraints
* **CPU First:** `device="cpu"` is explicitly enforced. `imgsz=320` ensures tensors remain small enough for quad-core processing without thermal throttling.
* **Modularity:** While the tracker logic moved inside the detector wrapper, the visualizer (`video_processor.py`) remains entirely unaware of PyTorch syntax, ensuring UI rendering and ML inference can be refactored independently.
