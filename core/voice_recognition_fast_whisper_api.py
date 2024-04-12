import utils.debug_utils as debug_utils
import utils.json_filter_utils as json_filter
import utils.audio_manipulation_utils as audio_mp
from faster_whisper import WhisperModel
import json
import datetime
from utils.datetime_utils import get_datetime_without_milliseconds
from tqdm import tqdm

def get_times_of_each_keyword_spoken(keyword, final_video_name, seconds_to_cut, combined_videos, useDebugFile = False):
    if useDebugFile is False:
        print(f"Initiating whisper process in {get_datetime_without_milliseconds(datetime.datetime.now())} for the video '{final_video_name}'")
        with open('config.json') as config_file:
            config = json.load(config_file)
            audio_enhenced_auth_path = audio_mp.generate_enhenced_audio(combined_videos, final_video_name)
            model = WhisperModel(config["whisper_model"], device="cpu", compute_type="int8")
            print("About extract the segments using fast whisper")
            segments, info  = model.transcribe(audio_enhenced_auth_path, language=config["language"], beam_size=5, best_of=5, word_timestamps=True)
            times_of_each_keyword_spoken = []
            for segment in segments:
                for word in segment.words:
                    show_progress_bar(segments, info)
                    end = word.end + 1
                    start = word.end  - seconds_to_cut
                    if(start < 0) :
                        start = 0
                        end = seconds_to_cut + 1
                    times_of_each_keyword_spoken.append({'start': start, 'end': end, 'text':word.word, 'confidence':word.probability})
            debug_utils.save_debug_file(times_of_each_keyword_spoken, final_video_name)
    else:
        times_of_each_keyword_spoken = debug_utils.get_debug_file(final_video_name)

    return json_filter.filter_json_by_keyword(times_of_each_keyword_spoken, keyword)

def show_progress_bar(segments, info):
    total_duration = round(info.duration, 2) 
    timestamps = 0.0  

    with tqdm(total=total_duration, unit=" audio seconds") as pbar:
        for segment in segments:
            pbar.update(segment.end - timestamps)
            timestamps = segment.end
        if timestamps < info.duration:
            pbar.update(info.duration - timestamps)