import utils.debug_utils as debug_utils
import utils.json_filter_utils as json_filter
import utils.audio_manipulation_utils as audio_mp
from faster_whisper import WhisperModel
import datetime
from utils.datetime_utils import get_datetime_without_milliseconds

def get_times_of_each_keyword_spoken(config, combined_videos):
    keyword = config['keyword']
    final_video_name = config['final_video_name']
    seconds_to_cut = config['seconds_to_cut']
    use_debug_file = config['use_debug_file']
    whisper_language = config['whisper_language']
    whisper_model = config['whisper_model']

    if not use_debug_file:
        print(f"Initiating whisper process at {get_datetime_without_milliseconds(datetime.datetime.now())} for the video '{final_video_name}'")
        
        audio_enhanced_path = audio_mp.generate_enhenced_audio(combined_videos, final_video_name)
        
        model = WhisperModel(whisper_model, device="cpu", compute_type="int8")
        
        print("Extracting segments using Fast Whisper")
        segments, _ = model.transcribe(audio_enhanced_path, language=whisper_language, beam_size=5, best_of=5, word_timestamps=True)
        
        times_of_each_keyword_spoken = []

        for segment in segments:
            for word in segment.words:
                end = word.end + 1
                start = max(word.end - seconds_to_cut, 0)
                
                if start == 0:
                    end = seconds_to_cut + 1
                
                times_of_each_keyword_spoken.append({
                    'start': start,
                    'end': end,
                    'text': word.word,
                    'confidence': word.probability
                })
        
        debug_utils.save_debug_file(times_of_each_keyword_spoken, final_video_name)
    else:
        times_of_each_keyword_spoken = debug_utils.get_debug_file(final_video_name)

    return json_filter.extract_keyword_occurrences(times_of_each_keyword_spoken, keyword)
