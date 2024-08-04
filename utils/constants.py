import tempfile
import os

TEMP_PATH = f"{tempfile.gettempdir()}{os.sep}automatic-video-edition" 
AUDIO_PATH = f"{TEMP_PATH}{os.sep}audio"
EXPORT_PATH = "export"
SAVED_RESULT_PATH = "result" 
VIDEO_GENERATION_PATH = f"{TEMP_PATH}{os.sep}video_generation"
MIN_VIDEO_SECONDS = 20