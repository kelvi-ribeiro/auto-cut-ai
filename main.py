
import core.video_manipulation_api as video_manipulation
import core.voice_recognition_api as voice_recognition
import utils.generic_utils as generic_utils
import json
import datetime as dt

def generate_cut_video(video_path, keyword, seconds_to_cut, useDebugFile):
    generic_utils.create_temp_dir()
    times_of_each_keyword_spoken = voice_recognition.get_times_of_each_keyword_spoken(keyword, video_path, useDebugFile)
    video_manipulation.generate_video(video_path, times_of_each_keyword_spoken, seconds_to_cut)
    generic_utils.remove_temp_dir()

with open('config.json') as config_file:
    config = json.load(config_file)

start_time = dt.datetime.now()
print(f"Initiating main process at {start_time}...")
generate_cut_video(config['video_path'], config['keyword'], config['seconds_to_cut'], config['useDebugFile'])
end_time = dt.datetime.now()

processing_time = (end_time - start_time).total_seconds() / 60
print(f"Finishing main process at {end_time}. Processing time: {processing_time:.2f} minutes.")