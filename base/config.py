"""Test harness config. Override any value via env var of the same name."""
import os

# LDPlayer instance 0 over adb. Instance 1 -> 127.0.0.1:5557, etc.
DEVICE_URI = os.environ.get("DEVICE_URI", "Android://127.0.0.1:5037/127.0.0.1:5555")

# Package name of the Unity puzzle game under test. Set before running real cases:
#   adb shell pm list packages | findstr <name>
APP_PACKAGE = os.environ.get("APP_PACKAGE", "com.example.puzzle")

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

# Where infra-drop evidence (jsonl + screenshots) is saved.
RESULTS_DIR = os.environ.get("RESULTS_DIR", os.path.join(os.path.dirname(__file__), "results"))
