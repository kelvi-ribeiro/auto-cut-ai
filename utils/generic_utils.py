import os
from utils.constants import TEMP_PATH, VIDEO_GENERATION_PATH, AUDIO_PATH, EXPORT_PATH, DEBUG_PATH

def create_functional_dir():
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)
    if not os.path.exists(DEBUG_PATH):
        os.makedirs(DEBUG_PATH)
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
        os.makedirs(VIDEO_GENERATION_PATH)
        os.makedirs(AUDIO_PATH)