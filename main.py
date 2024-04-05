
import core.video_manipulation_api as video_manipulation
import core.voice_recognition_api as voice_recognition
import json
import datetime

def generate_cut_video(video_path, keyword, seconds_to_cut, useDebugFile):
    times_of_each_keyword_spoken = voice_recognition.get_times_of_each_keyword_spoken(keyword, video_path, useDebugFile)
    video_manipulation.generate_video(video_path, times_of_each_keyword_spoken, seconds_to_cut)

with open('config.json') as config_file:
    config = json.load(config_file)

print(f"Initiating main process in {datetime.datetime.now()}...")
generate_cut_video(config['video_path'], config['keyword'], config['seconds_to_cut'], config['useDebugFile'])
print(f"Finishing main process in {datetime.datetime.now()}...")