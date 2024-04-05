import utils.debug_utils as debug_utils
import utils.json_filter_utils as json_filter
import whisper_timestamped as whisper
import json
import datetime

def get_times_of_each_keyword_spoken(keyword, video_path, useDebugFile = False):
    if useDebugFile is False:
        print(f"Initiating whisper process in {datetime.datetime.now()}...")
        audio = whisper.load_audio(video_path) 
        with open('config.json') as config_file:
            config = json.load(config_file)
            model = whisper.load_model(config["whisper_model"], device="cpu", in_memory = True)
            result = whisper.transcribe_timestamped(model, audio, language=config["language"], beam_size=5, best_of=5)
            print(f"Whisper processing finished in {datetime.datetime.now()}...")
            debug_utils.save_debug_file(result)
    else:
        result = debug_utils.get_debug_file()

    return json_filter.filter_json_by_keyword(result, keyword)