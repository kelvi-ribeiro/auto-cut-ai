
import core.video_manipulation_api as video_manipulation
import core.voice_recognition_fast_whisper_api as voice_recognition
import utils.generic_utils as generic_utils
import json
import datetime as dt
import os
from utils.constants import VIDEO_GENERATION_PATH
from utils.file_utils import get_filename_from_full_path
from utils.datetime_utils import get_datetime_without_milliseconds

def generate_cut_video(video_path, keyword, seconds_to_cut, useDebugFile): 
    print(f"About to process the video '{get_filename_from_full_path(video_path)}'")
    times_of_each_keyword_spoken = voice_recognition.get_times_of_each_keyword_spoken(keyword, video_path, useDebugFile)
    return video_manipulation.generate_video(video_path, times_of_each_keyword_spoken, seconds_to_cut)

def generate_final_video():
    totalCutsFound = 0
    generic_utils.create_temp_dir()
    start_time = dt.datetime.now()
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    print(f"Initiating main process at {get_datetime_without_milliseconds(start_time)}...")
    files = []
    if not config.get("videos_path_dir", ""):
        files.append(config['video_path'])
    else: 
        print(f"About to read the directory '{config["videos_path_dir"]}' to get all files")
        files = [os.path.join(config["videos_path_dir"], file) for file in os.listdir(config["videos_path_dir"]) if os.path.isfile(os.path.join(config["videos_path_dir"], file))]
    print(f"'{len(files)}' files were found to process with names: '{", ".join(list(map((lambda f: get_filename_from_full_path(f)), files)))}'")
    for file in files:
        totalCutsFound += generate_cut_video(file, config['keyword'], config['seconds_to_cut'], config['useDebugFile'])

    generated_cut_videos = [os.path.join(VIDEO_GENERATION_PATH, file) for file in os.listdir(VIDEO_GENERATION_PATH) if os.path.isfile(os.path.join(VIDEO_GENERATION_PATH, file))]

    video_manipulation.merge_videos(generated_cut_videos, config["final_video_name"])
    end_time = dt.datetime.now()
    processing_time = (end_time - start_time).total_seconds() / 60
    generic_utils.remove_temp_dir()
    print(f"Finishing main process at {get_datetime_without_milliseconds(end_time)}. ")
    print(f"Processing time: '{processing_time:.2f}' minutes with '{len(files)}' processed and '{totalCutsFound}' total cuts found.")