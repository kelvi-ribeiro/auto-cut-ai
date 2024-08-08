from core.recognition_processor import RecognitionProcessor
from faster_whisper import WhisperModel
from utils.datetime_utils import get_datetime_without_milliseconds
import datetime
import utils.audio_manipulation_utils as audio_mp
import utils.string_utils as string_utils

class VoiceRecognition(RecognitionProcessor):
    def __init__(self, files, config, notification_system, combined_videos):
        super().__init__(files, config, notification_system, combined_videos)

    def process(self):
        final_video_name = self.config['final_video_name']
        whisper_language = self.config['whisper_language']
        whisper_model = self.config['whisper_model']

        self.notification_system.notify(f"Initiating whisper process at {get_datetime_without_milliseconds(datetime.datetime.now())} for the video '{final_video_name}'")

        audio_enhanced_path = audio_mp.generate_enhenced_audio(self.combined_videos, final_video_name)

        model = WhisperModel(whisper_model, device="cpu", compute_type="int8")

        self.notification_system.notify("Extracting segments using Fast Whisper")
        segments, _ = model.transcribe(audio_enhanced_path, language=whisper_language, beam_size=5, best_of=5, word_timestamps=True)
        times_of_each_keyword_spoken = []

        for segment in segments:
            for word in segment.words:
                times_of_each_keyword_spoken.append({
                    'end': word.end + 1,
                    'text': word.word,
                    'confidence': word.probability
                })

        
        filtered_results = self.filter_according_with_keyword(times_of_each_keyword_spoken)
        for filtered_result in filtered_results:
            self.add_time_cut(filtered_result['end'])
        
        return self.get_times_cut_with_removed_duplicates()
            
    
    def filter_according_with_keyword(self, times_of_each_keyword_spoken): 
        keyword = self.config['keyword']
        minimum_confidence = self.config['minimum_confidence']
        filtered_results = []
        self.notification_system.notify(f"About to map the '{self.config['keyword']}' in result" )
        for word in times_of_each_keyword_spoken: 
            if string_utils.remove_special_chars_and_accents(keyword) in string_utils.remove_special_chars_and_accents(word['text']) and word['confidence'] > minimum_confidence:
                filtered_results.append(word)

        return filtered_results
