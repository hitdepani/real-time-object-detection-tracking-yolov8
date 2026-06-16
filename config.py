import yaml
from pathlib import Path

def load_config(config_path="configs/tracking_config.yaml"):
    """
    Loads configuration from a YAML file.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

# Load default config upon import
try:
    DEFAULT_CONFIG = load_config()
except FileNotFoundError:
    # Fallback to an empty dictionary or basic defaults if running in an unexpected working directory
    DEFAULT_CONFIG = {
        "detector": {"model_name": "yolov8n.pt", "conf_threshold": 0.25, "iou_threshold": 0.45, "imgsz": 320, "classes": [0, 2]},
        "tracker": {"track_thresh": 0.25, "track_buffer": 30, "match_thresh": 0.8, "skip_frames": 2},
        "visualizer": {"line_thickness": 2, "font_scale": 0.5, "draw_trails": True, "trail_length": 30},
        "logging": {"save_csv": True, "console_verbosity": "INFO"}
    }

DETECTOR_CONFIG = DEFAULT_CONFIG.get("detector", {})
TRACKER_CONFIG = DEFAULT_CONFIG.get("tracker", {})
VISUALIZER_CONFIG = DEFAULT_CONFIG.get("visualizer", {})
LOGGING_CONFIG = DEFAULT_CONFIG.get("logging", {})

# Notes for Future AI Assistants
# Purpose of the file: Loads the `configs/tracking_config.yaml` file and exposes its parameters globally.
# Key dependencies: `yaml` (pyyaml), `pathlib`.
# Extension points: Can be extended to support data validation (e.g., using Pydantic) or to allow runtime updates from CLI arguments.
# Architectural constraints: Must remain completely independent of other project modules to prevent circular imports. Configuration should be treated as read-only.
