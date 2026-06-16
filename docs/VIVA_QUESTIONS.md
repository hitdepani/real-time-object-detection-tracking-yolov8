# docs/VIVA_QUESTIONS.md - Academic Viva Preparation Guide

This document contains a comprehensive list of potential questions that external examiners may ask during academic project evaluations, along with detailed, architecturally sound responses.

---

## Part 1: Architecture and System Design

### 1. Explain the execution flow of your pipeline.
**Answer:** 
The application utilizes a multi-threaded pipe-and-filter pipeline:
1.  **Frame Ingestion (I/O Thread)**: A background thread captures frames from the source (webcam or video file) using OpenCV and buffers them in a thread-safe Queue of size 30. This ensures that I/O wait times do not bottleneck CPU processing.
2.  **Preprocessing**: The main thread de-queues a frame, resizes it to a square matrix (default `320x320` or `416x416` for CPU speed), and normalizes it.
3.  **Inference**: The preprocessed image is fed to YOLOv8n, yielding a collection of class-associated bounding boxes, which are filtered by confidence and class IDs.
4.  **Tracking (ByteTrack)**: The detections are passed to the tracker, which applies Kalman Filter state predictions and matches them via Hungarian Association (with double-association for low-confidence boxes).
5.  **Visualization & Logging**: The visualizer overlays the tracking details and motion history paths onto the frame, which is rendered to screen and queued for disk storage. Telemetry counters write execution stats to a CSV log.

### 2. Why did you choose a multi-threaded approach for video ingestion?
**Answer:**
In OpenCV, `cap.read()` blocks execution until a frame is delivered by the hardware (webcam) or decoded from disk. In a single-threaded system, this I/O delay is added to the inference time, reducing FPS. By separating ingestion into a background thread, the next frame is always ready in RAM memory before the detector requests it.

---

## Part 2: Object Detection and YOLOv8

### 3. What does YOLO stand for, and how does it differ from older architectures (like R-CNN)?
**Answer:**
YOLO stands for **You Only Look Once**.
*   **Older Architectures (e.g., Faster R-CNN)**: Use a two-stage approach. First, a Region Proposal Network (RPN) proposes candidate regions. Second, a classifier processes each region. This is highly accurate but computationally expensive and slow.
*   **YOLO**: A one-stage detector. It frames object detection as a single regression problem, predicting bounding box coordinates and class probabilities directly from full images in a single forward pass, making it fast enough for real-time applications.

### 4. What are the key improvements in YOLOv8 compared to YOLOv5?
**Answer:**
1.  **Anchor-Free Design**: YOLOv5 is anchor-based, requiring predefined anchor boxes. YOLOv8 is anchor-free, predicting the center of an object directly, which reduces the complexity of the bounding box regression head.
2.  **New Backbone & Neck**: Uses a C2f module (coarse-to-fine) instead of C3, which improves feature aggregation and gradient flow.
3.  **Decoupled Head**: Separates the classification and localization tasks into individual branches, which increases overall precision.

### 5. Why is YOLOv8n (nano) chosen over larger variants (YOLOv8s, YOLOv8m)?
**Answer:**
*   YOLOv8n is designed for edge deployment and resource-constrained environments.
*   It has only **3.2 Million parameters** (compared to YOLOv8s' 11.2M and YOLOv8x' 68.2M).
*   It requires **8.7 GFLOPs**, making it fast enough to run on CPUs. Larger variants would drop frame rates to single digits on older CPU-only hardware.

---

## Part 3: Object Tracking and ByteTrack

### 6. What is the fundamental difference between Object Detection and Object Tracking?
**Answer:**
*   **Object Detection**: Operates on a single frame. It identifies *what* and *where* objects are, but does not know if a person in frame 1 is the same person in frame 2. It has no memory.
*   **Object Tracking**: Links detections across consecutive frames over time. It assigns a persistent tracking ID (e.g. ID #4) to an object, enabling path prediction and count features.

### 7. What is the core innovation of ByteTrack?
**Answer:**
ByteTrack's core innovation is its **double association** matching method.
Most traditional trackers (like DeepSORT) discard low-confidence detections (e.g., confidence < 0.5) to avoid false positives. However, this causes tracking loss during occlusion, shadow, or blur when confidence naturally drops.
*   ByteTrack first associates high-confidence detections with existing tracks.
*   It then performs a **second association** matching the *remaining* unmatched tracks against the *low-confidence* detections. This recovers lost targets without introducing background noise.

### 8. Why was ByteTrack selected over DeepSORT for a CPU-only project?
**Answer:**
*   **DeepSORT** requires a deep Re-Identification (Re-ID) neural network to extract appearance features for matching. Running this neural network on every detected object requires significant CPU/GPU processing.
*   **ByteTrack** matches objects using Intersection over Union (IoU) overlap and Kalman Filter motion predictions. By removing deep feature extraction, ByteTrack runs in less than 2ms per frame on CPU, compared to 20-50ms for DeepSORT.

### 9. Explain the role of the Kalman Filter and the Hungarian Algorithm in tracking.
**Answer:**
*   **Kalman Filter**: Predicts the next state (position and velocity) of an active track based on its previous motion. This provides a search region in the next frame.
*   **Hungarian Algorithm**: Solves the assignment problem. It calculates the optimal pairings between predicted track locations and incoming detections by maximizing the Intersection over Union (IoU) metric.

---

## Part 4: CPU Optimization Strategies

### 10. How did you optimize the pipeline to run on an older CPU?
**Answer:**
1.  **Reduced Inference Resolution**: Downscaling input frames from the default `640x640` to `320x320` reduces pixel processing requirements by 75%, accelerating inference.
2.  **Frame Skipping**: Running YOLOv8 detection only on every $N$-th frame (e.g. every 2nd or 3rd frame). On skipped frames, the tracker uses Kalman Filter motion predictions to update target coordinates, skipping model inference to save CPU cycles.
3.  **Threaded Ingestion**: Decouples webcam read blocking from model inference.
4.  **No-Grad Execution**: Bypasses gradient graph generation during PyTorch runtimes, reducing RAM overhead.
