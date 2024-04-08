
import core.video_manipulation_api as video_manipulation
import core.voice_recognition_fast_whisper_api as voice_recognition
import utils.generic_utils as generic_utils
import json
import datetime as dt
import os
from utils.constants import VIDEO_GENERATION_PATH
from utils.file_utils import get_filename_from_full_path
from utils.datetime_utils import get_datetime_without_milliseconds
from utils.email_utils import send_email

def generate_cut_video(video_path, keyword, seconds_to_cut, useDebugFile, config, index, filesLen): 
    about_to_process_message = f"About to process the video '{get_filename_from_full_path(video_path)}' of {index + 1}/{filesLen}. "
    print(about_to_process_message)
    send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} update process status", about_to_process_message)
    times_of_each_keyword_spoken = voice_recognition.get_times_of_each_keyword_spoken(keyword, video_path, seconds_to_cut, useDebugFile)
    return video_manipulation.generate_video(video_path, times_of_each_keyword_spoken, seconds_to_cut)

def generate_final_video():
    totalCutsFound = 0
    generic_utils.create_temp_dir()
    start_time = dt.datetime.now()
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    print(f"Initiating main process at {get_datetime_without_milliseconds(start_time)}...")
    try:
        files = []
        if not config.get("videos_path_dir", ""):
            files.append(config['video_path'])
        else: 
            print(f"About to read the directory '{config["videos_path_dir"]}' to get all files")
            files = [os.path.join(config["videos_path_dir"], file) for file in os.listdir(config["videos_path_dir"]) if os.path.isfile(os.path.join(config["videos_path_dir"], file))]
        print(f"'{len(files)}' files were found to process with names: '{", ".join(list(map((lambda f: get_filename_from_full_path(f)), files)))}'")
        for index, file in enumerate(files):
            totalCutsFound += generate_cut_video(file, config['keyword'], config['seconds_to_cut'], config['useDebugFile'], config, index , len(files))

        cut_videos_message = f"All videos were processed, about to merges all videos in '{config["final_video_name"]}'"
        print(cut_videos_message)
        send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} update process status", cut_videos_message)
        generated_cut_videos = [os.path.join(VIDEO_GENERATION_PATH, file) for file in os.listdir(VIDEO_GENERATION_PATH) if os.path.isfile(os.path.join(VIDEO_GENERATION_PATH, file))]
    
        video_manipulation.merge_videos(generated_cut_videos, config["final_video_name"])
        end_time = dt.datetime.now()
        processing_time = (end_time - start_time).total_seconds() / 60
        generic_utils.remove_temp_dir()
        finalLogMessage = f"Finishing main process at {get_datetime_without_milliseconds(end_time)}.\n Processing time: '{processing_time:.2f}' minutes, with '{len(files)}' videos processed and '{totalCutsFound}' total cuts found."
        print(finalLogMessage)
        send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} processed", finalLogMessage)
    except Exception as e:
        send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} not processed", f"Error trying to process {config["final_video_name"]}, with exception message {str(e)}")
        raise e
    