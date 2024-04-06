import os
import shutil
from utils.constants import TEMP_PATH

def create_temp_dir():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

def remove_temp_dir():
    shutil.rmtree(TEMP_PATH)