import os
import cv2
import time
import logging
from datetime import datetime
from pathlib import Path

def setup_directories():
    """Create required directories if they do not exist."""
    directories = ["outputs", "snapshots", "logs"]
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)

def setup_logging(log_file_prefix="app_log"):
    """Configure application logging to terminal and a log file."""
    setup_directories()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{log_file_prefix}_{timestamp}.log"
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def validate_video_path(video_path):
    """Validates if the provided video file exists."""
    path = Path(video_path)
    if not path.is_file():
        raise FileNotFoundError(f"Video file not found at: {video_path}")
    return str(path)

def save_snapshot(frame, prefix="snapshot"):
    """Saves a single frame to the snapshots directory."""
    setup_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"snapshots/{prefix}_{timestamp}.jpg"
    success = cv2.imwrite(filename, frame)
    if success:
        logging.info(f"Snapshot saved to: {filename}")
    else:
        logging.error(f"Failed to save snapshot to: {filename}")

def generate_timestamped_filename(base_name, extension=".mp4"):
    """Generates a unique filename with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

class FPSCounter:
    """Calculates smoothed frames per second using a moving average."""
    def __init__(self, history_size=30):
        self.history_size = history_size
        self.history = []
        self.last_time = None
        self.fps = 0.0

    def start(self):
        self.last_time = time.time()

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        if dt > 0:
            self.history.append(1.0 / dt)
            if len(self.history) > self.history_size:
                self.history.pop(0)
            self.fps = sum(self.history) / len(self.history)

    def get_fps(self):
        return self.fps

# Notes for Future AI Assistants
# Purpose: Shared stateless utilities (I/O, FPS tracking, logging).
# Refactored: FPSCounter now uses a moving average window (`history_size`) for much smoother UI updates.
