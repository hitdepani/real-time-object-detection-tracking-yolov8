# Testing Guide

## 1. Webcam Test Procedure
Command: `python main.py --webcam`
* Stand in front of the camera. Verify a bounding box appears around you with the label `person` and a unique `ID`.
* Walk out of the frame and return. Verify that the tracking logic correctly assigns a *new* ID or recovers the old one (if within the `track_buffer` timeout).
* Press `q` to gracefully close the application. Check `logs/` to confirm a successful shutdown trace.

## 2. Video File Test Procedure
Command: `python main.py --video sample.mp4` (Assuming `sample.mp4` exists).
* Verify the video plays through entirely.
* Observe the FPS counter in the top-left corner. It should remain stable due to the moving-average optimization.

## 3. Snapshot Validation
Command: `python main.py --webcam`
* While running, press `s` on the keyboard.
* Open the `snapshots/` directory in your file explorer. Verify a `.jpg` image containing the *annotated* frame (boxes included) was saved.

## 4. Output Video Validation
Command: `python main.py --webcam --save-output`
* Run the script for 10 seconds. Press `q`.
* Open the `outputs/` directory. Play the resulting `.mp4` file in VLC or Windows Media Player. Verify the video is not corrupted and contains tracking annotations.

## 5. Expected Console Logs
* `Initializing ObjectDetector with model: yolov8n.pt on CPU`
* `Starting pipeline in webcam mode.`
* `Video I/O resources released. Processing finished.`
* `Application closed successfully.`

## 6. Common Failure Modes
* **SystemExit / argparse errors:** Passing both `--webcam` and `--video` simultaneously will cause `argparse` to cleanly exit with an error instructing the user to pick one.
* **File Not Found:** Providing a bad path to `--video` triggers the `validate_video_path` utility, printing a clean console error rather than a raw python stack trace.
* **Corrupted Video Feed:** If the webcam disconnects mid-stream, the `try/except` loop inside `video_processor.py` catches the empty frame and logs `End of video stream.`, terminating gracefully.
