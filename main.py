import sys
import argparse
import logging

from utils import setup_logging, validate_video_path
from video_processor import VideoProcessor

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Real-Time Object Detection and Tracking Using YOLOv8 and ByteTrack (Ultralytics Built-in)"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--webcam", action="store_true", help="Use the default system webcam.")
    group.add_argument("--video", type=str, metavar="PATH", help="Path to input video file.")
    
    parser.add_argument("--save-output", action="store_true", help="Save the processed video to outputs/.")
    parser.add_argument("--no-display", action="store_true", help="Run in headless mode.")
    return parser.parse_args()

def main():
    logger = setup_logging(log_file_prefix="tracking_run")
    
    try:
        args = parse_arguments()
    except SystemExit as e:
        sys.exit(e.code)
        
    source = None
    if args.webcam:
        source = 0
        logger.info("Starting pipeline in webcam mode.")
    elif args.video:
        try:
            source = validate_video_path(args.video)
            logger.info(f"Starting pipeline in video mode: {source}")
        except Exception as e:
            logger.error(f"Invalid video path: {e}")
            print(f"ERROR: {e}")
            sys.exit(1)
            
    try:
        processor = VideoProcessor(source=source, save_output=args.save_output, no_display=args.no_display)
        processor.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print("FATAL ERROR. Check logs/ for details.")
        sys.exit(1)
        
    logger.info("Application closed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()

# Notes for Future AI Assistants
# Purpose: CLI Entry point.
# Refactored: Maintained previous structure, updated descriptive text to reflect new built-in tracking architecture.
