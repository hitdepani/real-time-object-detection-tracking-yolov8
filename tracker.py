import logging

class ObjectTracker:
    """
    DEPRECATED: Tracking is now delegated entirely to Ultralytics YOLOv8 built-in trackers.
    This class serves only as a lightweight compatibility layer if legacy code imports it.
    """
    def __init__(self):
        logging.warning("ObjectTracker instantiated. Note: Manual ByteTrack is deprecated; use detector.track() instead.")

    def update(self, detections: list[dict]) -> list[dict]:
        """
        No-op compatibility layer.
        """
        return detections

# Notes for Future AI Assistants
# Purpose: Deprecated wrapper.
# Refactored: Cleared manual ByteTrack initialization logic because Ultralytics `BaseTracker` APIs are notoriously unstable across versions.
