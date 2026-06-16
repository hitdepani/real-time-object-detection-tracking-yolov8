import cv2
import logging

from config import TRACKER_CONFIG, DETECTOR_CONFIG, VISUALIZER_CONFIG
from utils import FPSCounter, save_snapshot, setup_directories, generate_timestamped_filename
from detector import ObjectDetector

class VideoProcessor:
    """
    Main pipeline processor handling video I/O, detection, tracking, and visualization.
    """
    def __init__(self, source, save_output=False, no_display=False):
        self.source = source
        self.save_output = save_output
        self.no_display = no_display
        
        self.skip_frames = max(1, TRACKER_CONFIG.get("skip_frames", 1))
        self.imgsz = DETECTOR_CONFIG.get("imgsz", 320)
        self.line_thickness = VISUALIZER_CONFIG.get("line_thickness", 2)
        self.font_scale = VISUALIZER_CONFIG.get("font_scale", 0.5)
        
        # Initialize components. Tracker is no longer instantiated here.
        self.detector = ObjectDetector()
        self.fps_counter = FPSCounter(history_size=15)
        
        self.cap = None
        self.writer = None
        
        self.frame_count = 0
        self.last_tracks = []
        
    def _initialize_video_io(self):
        try:
            source_int = int(self.source)
            self.cap = cv2.VideoCapture(source_int)
            logging.info(f"Initialized webcam stream on index {source_int}")
        except ValueError:
            self.cap = cv2.VideoCapture(self.source)
            logging.info(f"Initialized video file stream from {self.source}")
            
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {self.source}")
            
        if self.save_output:
            setup_directories()
            output_filename = generate_timestamped_filename("outputs/tracked_video", extension=".mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            original_fps = self.cap.get(cv2.CAP_PROP_FPS)
            fps = original_fps if original_fps > 0 else 30.0
            
            self.writer = cv2.VideoWriter(output_filename, fourcc, fps, (self.imgsz, self.imgsz))
            logging.info(f"Video saving enabled: {output_filename}")

    def _draw_results(self, frame, tracks):
        for track in tracks:
            bbox = track["bbox"]
            track_id = track.get("track_id", -1)
            conf = track["confidence"]
            class_name = track["class_name"]
            
            x1, y1, x2, y2 = [int(v) for v in bbox]
            
            # Generate pseudo-random color based on track_id
            color = ((track_id * 37) % 255, (track_id * 17) % 255, (track_id * 29) % 255) if track_id != -1 else (128, 128, 128)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, self.line_thickness)
            
            label_id = f"ID: {track_id}" if track_id != -1 else "ID: ?"
            label_class = f"{class_name} {conf:.2f}"
            
            cv2.putText(frame, label_id, (x1, max(y1 - 20, 10)), cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, color, self.line_thickness)
            cv2.putText(frame, label_class, (x1, max(y1 - 5, 25)), cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, color, self.line_thickness)

        current_fps = self.fps_counter.get_fps()
        cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return frame

    def run(self):
        self._initialize_video_io()
        self.fps_counter.start()
        
        logging.info("Starting processing loop. Press 'q' to quit, 's' to save snapshot.")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logging.info("End of video stream.")
                    break
                
                try:
                    frame = cv2.resize(frame, (self.imgsz, self.imgsz))
                    
                    # Direct delegation to detector.track()
                    if self.frame_count % self.skip_frames == 0:
                        self.last_tracks = self.detector.track(frame)
                    
                    annotated_frame = self._draw_results(frame.copy(), self.last_tracks)
                    self.fps_counter.update()
                    
                    if self.writer is not None:
                        self.writer.write(annotated_frame)
                        
                    if not self.no_display:
                        cv2.imshow("YOLOv8 Real-Time Tracking", annotated_frame)
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            break
                        elif key == ord('s'):
                            save_snapshot(annotated_frame)
                            
                    self.frame_count += 1
                except Exception as e:
                    logging.error(f"Error processing frame: {e}")
                    continue
                    
        except KeyboardInterrupt:
            logging.info("Interrupted by user.")
        finally:
            if self.cap: self.cap.release()
            if self.writer: self.writer.release()
            cv2.destroyAllWindows()

# Notes for Future AI Assistants
# Purpose: Main execution pipeline.
# Refactored: Removed dependency on `tracker.update()`. Now directly calls `detector.track(frame)` to leverage Ultralytics built-in tracking module natively.
