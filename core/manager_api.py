
import core.video_manipulation_api as video_manipulation
import core.voice_recognition_fast_whisper_api as voice_recognition
import utils.generic_utils as generic_utils
import json
import datetime as dt
import os
from utils.constants import EXPORT_PATH
from utils.datetime_utils import get_datetime_without_milliseconds
from utils.number_utils  import get_pretty_minutes
from utils.email_utils import send_email

def generate_cut_video(keyword, seconds_to_cut, useDebugFile, config, dir_to_save, combined_videos): 
    about_to_process_message = f"About to process the video '{config["final_video_name"]}'. "
    print(about_to_process_message)
    send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} update process status", about_to_process_message)
    times_of_each_keyword_spoken = voice_recognition.get_times_of_each_keyword_spoken(keyword, config["final_video_name"], seconds_to_cut, combined_videos, useDebugFile)
    return video_manipulation.generate_video(combined_videos, times_of_each_keyword_spoken, dir_to_save, config["final_video_name"], config["masks_config"])

def generate_final_video():
    totalCutsFound = 0
    generic_utils.create_temp_dir()
    start_time = dt.datetime.now()
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    print(f"Initiating main process at {get_datetime_without_milliseconds(start_time)}...")
    try:
        print(f"About to merge all videos to not have problems with cuts between the videos")
        files = [os.path.join(config["videos_path_dir"], file) for file in os.listdir(config["videos_path_dir"]) if os.path.isfile(os.path.join(config["videos_path_dir"], file))]
        combined_videos = video_manipulation.merge_videos(files)
        (totalCutsFound, sum_seconds_total_video) = generate_cut_video(config['keyword'], config['seconds_to_cut'], config['useDebugFile'], config, EXPORT_PATH, combined_videos)
        end_time = dt.datetime.now()
        processing_time = (end_time - start_time).total_seconds() / 60
        finalLogMessage = f"Finishing main process at {get_datetime_without_milliseconds(end_time)}.\n Processing time: '{processing_time:.2f}' minutes\n'{len(files)}' videos processed and '{totalCutsFound}' total cuts found and '{get_pretty_minutes(sum_seconds_total_video / 60)}' minutes of video."
        print(finalLogMessage)
        send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} processed", finalLogMessage)
    except Exception as e:
        send_email(config["email_no_reply"], config["email_to"], config["password_no_reply"], f"{config["final_video_name"]} not processed", f"Error trying to process {config["final_video_name"]}, with exception message {str(e)}")
        raise e
    