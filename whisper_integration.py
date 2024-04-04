import re
import whisper_timestamped as whisper

def get_json_timestamped_result(keyword, filepath):
    audio = whisper.load_audio(filepath)

    model = whisper.load_model("tiny", device="cpu")

    result = whisper.transcribe(model, audio, language="pt")
    return filter_json_by_keyword(result, keyword)

def filter_json_by_keyword(json_data, keyword):
    if not keyword:
        return map_json_data(json_data)
    
    only_words_array = map_json_data(json_data)
    filtered_results = []
    for word in only_words_array:
        word_text = re.sub('[^A-Za-z0-9]+', '', word["text"]).lower() 
        if keyword.lower() in word_text:
            filtered_results.append(word)

    return filtered_results

def map_json_data(json_data):
    mapped_array = []
    for segment in json_data["segments"]:
        for word in segment["words"]:
          mapped_array.append(word)

    return mapped_array