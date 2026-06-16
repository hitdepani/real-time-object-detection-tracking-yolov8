import logging
import numpy as np
from ultralytics import YOLO

# Load configurations
from config import DETECTOR_CONFIG

class ObjectDetector:
    """
    Lightweight wrapper around the YOLOv8 model tailored for CPU inference.
    Now leverages built-in Ultralytics tracking logic.
    """
    def __init__(self):
        self.model_name = DETECTOR_CONFIG.get("model_name", "yolov8n.pt")
        self.conf_threshold = DETECTOR_CONFIG.get("conf_threshold", 0.25)
        self.iou_threshold = DETECTOR_CONFIG.get("iou_threshold", 0.45)
        self.imgsz = DETECTOR_CONFIG.get("imgsz", 320)
        self.target_classes = DETECTOR_CONFIG.get("classes", None)

        logging.info(f"Initializing ObjectDetector with model: {self.model_name} on CPU")
        
        try:
            self.model = YOLO(self.model_name)
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            raise RuntimeError(f"Model Initialization failed.") from e

    def detect(self, frame: np.ndarray) -> list[dict]:
        """Runs standard detection without tracking."""
        detections = []
        try:
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                imgsz=self.imgsz,
                classes=self.target_classes,
                device="cpu",
                verbose=False
            )
            result = results[0]
            boxes = result.boxes
            if boxes is None or len(boxes) == 0:
                return detections

            xyxy = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy()
            cls_ids = boxes.cls.cpu().numpy().astype(int)

            for box, conf, cls_id in zip(xyxy, confs, cls_ids):
                class_name = self.model.names.get(cls_id, str(cls_id))
                detections.append({
                    "bbox": [float(box[0]), float(box[1]), float(box[2]), float(box[3])],
                    "confidence": float(conf),
                    "class_id": int(cls_id),
                    "class_name": class_name
                })
        except Exception as e:
            logging.error(f"Inference error during detection: {e}")
        return detections

    def track(self, frame: np.ndarray) -> list[dict]:
        """
        Runs YOLOv8 built-in tracking (ByteTrack) on a single frame.
        Maintains internal state via persist=True.
        """
        tracked_objects = []
        try:
            results = self.model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                imgsz=self.imgsz,
                classes=self.target_classes,
                device="cpu",
                verbose=False
            )
            
            result = results[0]
            boxes = result.boxes
            if boxes is None or len(boxes) == 0:
                return tracked_objects
            
            xyxy = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy()
            cls_ids = boxes.cls.cpu().numpy().astype(int)
            
            # Extract track IDs (might be None if no objects are stably tracked yet)
            track_ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else [-1]*len(boxes)

            for box, conf, cls_id, track_id in zip(xyxy, confs, cls_ids, track_ids):
                if track_id == -1:
                    continue # Skip objects that haven't been assigned an ID by the tracker
                    
                class_name = self.model.names.get(cls_id, str(cls_id))
                tracked_objects.append({
                    "track_id": int(track_id),
                    "bbox": [float(box[0]), float(box[1]), float(box[2]), float(box[3])],
                    "confidence": float(conf),
                    "class_id": int(cls_id),
                    "class_name": class_name
                })
        except Exception as e:
            logging.error(f"Tracking error: {e}")
            
        return tracked_objects

# Notes for Future AI Assistants
# Purpose: Core YOLOv8 inference wrapper.
# Refactored: Introduced `track()` method to delegate ByteTrack directly to Ultralytics internal engine `model.track()`. This fixes previous manual tracker API mismatches.
