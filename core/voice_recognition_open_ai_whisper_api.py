import utils.debug_utils as debug_utils
import utils.json_filter_utils as json_filter
import whisper_timestamped as whisper
import utils.audio_manipulation_utils as audio_mp
import json
import datetime

def get_times_of_each_keyword_spoken(keyword, video_path, seconds_to_cut, useDebugFile = False):
    if useDebugFile is False:
        print(f"Initiating whisper process in {datetime.datetime.now()}...")
        with open('config.json') as config_file:
            config = json.load(config_file)
            audio_enhenced_auth_path = audio_mp.generate_enhenced_audio(video_path)
            model = whisper.load_model(config["whisper_model"], device="cpu", in_memory = True)
            result = whisper.transcribe_timestamped(model, audio_enhenced_auth_path, language=config["language"], beam_size=5, best_of=5)
            print(f"Whisper processing finished in {datetime.datetime.now()}...")
            result = map_json_data(result)
            debug_utils.save_debug_file(result)
    else:
        result = debug_utils.get_debug_file()

    return json_filter.filter_json_by_keyword(result, keyword, seconds_to_cut)

def map_json_data(json_data):
    mapped_array = []
    for segment in json_data["segments"]:
        for word in segment["words"]:
          mapped_array.append(word)

    return mapped_array