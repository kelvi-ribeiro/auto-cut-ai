import utils.debug_utils as debug_utils
import utils.json_filter_utils as json_filter
import utils.audio_manipulation_utils as audio_mp
from faster_whisper import WhisperModel
import json
import datetime
from utils.file_utils import get_filename_from_full_path
from utils.datetime_utils import get_datetime_without_milliseconds

def get_times_of_each_keyword_spoken(keyword, video_path, seconds_to_cut, useDebugFile = False):
    if useDebugFile is False:
        print(f"Initiating whisper process in {get_datetime_without_milliseconds(datetime.datetime.now())} for the video {get_filename_from_full_path(video_path)}")
        with open('config.json') as config_file:
            config = json.load(config_file)
            audio_enhenced_auth_path = audio_mp.generate_enhenced_audio(video_path)
            model = WhisperModel(config["whisper_model"], device="cpu", compute_type="int8")
            segments, _  = model.transcribe(audio_enhenced_auth_path, language=config["language"], beam_size=5, best_of=5, word_timestamps=True)
            times_of_each_keyword_spoken = []

            for segment in segments:
                for word in segment.words:
                    times_of_each_keyword_spoken.append({'start': word.start, 'end':word.end, 'text':word.word, 'confidence':word.probability})
            debug_utils.save_debug_file(times_of_each_keyword_spoken, video_path)
    else:
        times_of_each_keyword_spoken = debug_utils.get_debug_file(video_path)

    return json_filter.filter_json_by_keyword(times_of_each_keyword_spoken, keyword, seconds_to_cut)