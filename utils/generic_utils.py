import os
from utils.constants import TEMP_PATH, VIDEO_GENERATION_PATH, AUDIO_PATH, EXPORT_PATH, SAVED_RESULT_PATH

def create_functional_dir():
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)
    if not os.path.exists(SAVED_RESULT_PATH):
        os.makedirs(SAVED_RESULT_PATH)
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
        os.makedirs(VIDEO_GENERATION_PATH)
        os.makedirs(AUDIO_PATH)