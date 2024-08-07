
import core.video_manipulation_api as video_manipulation
from core.gesture_recognition.gesture_recognition import GestureRecognition
from core.screen_color_recognition import ScreenColorRecognition
from core.voice_recognition import VoiceRecognition
import utils.generic_utils as generic_utils
import datetime as dt
import os
from utils.constants import EXPORT_PATH
from utils.datetime_utils import get_datetime_without_milliseconds
from utils.number_utils  import get_pretty_minutes
from utils.email_utils import send_email
from utils.file_utils import get_result_file, save_result_file

def generate_cut_video(config, files, dir_to_save, combined_videos): 
    recognition_type = config["recognition_type"]
    use_saved_result_file = config["use_saved_result_file"]
    final_video_name = config["final_video_name"]
    about_to_process_message = f"About to process the video '{final_video_name}'. "
    print(about_to_process_message)
    send_email(config, f"{final_video_name} update process status", about_to_process_message)
    times_of_each_cut = []
    if not use_saved_result_file:
        if recognition_type == "voice_recognition":
            recognition_processor = VoiceRecognition(files, config, combined_videos)
        elif recognition_type == "gesture_recognition":
            recognition_processor = GestureRecognition(files, config)
        else: 
            recognition_processor = ScreenColorRecognition(files, config)
            
        times_of_each_cut = recognition_processor.process()
        save_result_file(times_of_each_cut, final_video_name)
    else:
        times_of_each_cut = get_result_file(final_video_name)
    return video_manipulation.generate_video(combined_videos, times_of_each_cut, dir_to_save, config)

def generate_final_video(config):
    totalCutsFound = 0
    generic_utils.create_functional_dir()
    start_time = dt.datetime.now()
    
    print(f"Initiating main process at {get_datetime_without_milliseconds(start_time)}...")
    try:
        print("About to merge all videos to not have problems with cuts between the videos")
        files = [os.path.join(config['videos_path_dir'], file) for file in os.listdir(config['videos_path_dir']) if os.path.isfile(os.path.join(config['videos_path_dir'], file))]
        combined_videos = video_manipulation.merge_videos(files)
        (totalCutsFound, sum_seconds_total_video) = generate_cut_video(config, files, EXPORT_PATH, combined_videos)
        end_time = dt.datetime.now()
        processing_time = (end_time - start_time).total_seconds() / 60
        finalLogMessage = f"Finishing main process at {get_datetime_without_milliseconds(end_time)}.\n Processing time: '{processing_time:.2f}' minutes\n'{len(files)}' videos processed and '{totalCutsFound}' total cuts found and '{get_pretty_minutes(sum_seconds_total_video / 60)}' minutes of video."
        print(finalLogMessage)
        send_email(config, f"{config['final_video_name']} processed", finalLogMessage)
    except Exception as e:
        send_email(config, f"{config['final_video_name']} not processed", f"Error trying to process {config['final_video_name']}, with exception message {str(e)}")
        raise e
    
def generate_final_video(config):
    totalCutsFound = 0
    generic_utils.create_functional_dir()
    start_time = dt.datetime.now()    
    print(f"Initiating main process at {get_datetime_without_milliseconds(start_time)}...")
    try:
        print("About to merge all videos to not have problems with cuts between the videos")
        files = [os.path.join(config['videos_path_dir'], file) for file in os.listdir(config['videos_path_dir']) if os.path.isfile(os.path.join(config['videos_path_dir'], file))]
        combined_videos = video_manipulation.merge_videos(files)
        (totalCutsFound, sum_seconds_total_video) = generate_cut_video(config, files, EXPORT_PATH, combined_videos)
        end_time = dt.datetime.now()
        processing_time = (end_time - start_time).total_seconds() / 60
        finalLogMessage = f"Finishing main process at {get_datetime_without_milliseconds(end_time)}.\n Processing time: '{processing_time:.2f}' minutes\n'{len(files)}' videos processed and '{totalCutsFound}' total cuts found and '{get_pretty_minutes(sum_seconds_total_video / 60)}' minutes of video."
        print(finalLogMessage)
        send_email(config, f"{config['final_video_name']} processed", finalLogMessage)
    except Exception as e:
        send_email(config, f"{config['final_video_name']} not processed", f"Error trying to process {config['final_video_name']}, with exception message {str(e)}")
        raise e
    