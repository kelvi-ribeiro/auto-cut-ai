import os
import shutil
from utils.constants import TEMP_PATH, VIDEO_GENERATION_PATH, AUDIO_PATH

def create_temp_dir():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
        os.makedirs(VIDEO_GENERATION_PATH)
        os.makedirs(AUDIO_PATH)

def remove_temp_dir():
    shutil.rmtree(TEMP_PATH)