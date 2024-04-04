import whisper_timestamped as whisper

def get_json_timestamped_result(keyword):
    audio = whisper.load_audio("Recording.m4a")

    model = whisper.load_model("tiny", device="cpu")

    result = whisper.transcribe(model, audio, language="pt")
    return filter_json_by_keyword(result, keyword)

def filter_json_by_keyword(json_data, keyword):
    if not keyword:
        return map_json_data(json_data)
    
    only_words_array = map_json_data(json_data)
    filtered_results = []
    for word in only_words_array: 
        if keyword in word["text"]:
            filtered_results.append(word)

    return filtered_results

def map_json_data(json_data):
    mapped_array = []
    for segment in json_data["segments"]:
        for word in segment["words"]:
          mapped_array.append(word)

    return mapped_array