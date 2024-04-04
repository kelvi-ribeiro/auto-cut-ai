import re
import unicodedata
import whisper_timestamped as whisper
import io, json

def remove_special_chars_and_accents(text):
    # Remove caracteres especiais
    text = re.sub(r'[^\w\s]', '', text)

    # Remove acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    return text.lower()

def get_json_timestamped_result(keyword, filepath, useDebugFile = False):
    if useDebugFile is False:
        audio = whisper.load_audio(filepath)
        model = whisper.load_model("openai/whisper-large-v3", device="cpu")
        result = whisper.transcribe(model, audio, language="pt", beam_size=5, best_of=5)
        # TODO REMOVER OU COLOCAR COMO VARIÁVEL DE AMBIENTE PARA SALVAR APENAS EM DESENVOLVIMENTO
        json_data = json.dumps(result, indent=4, ensure_ascii=False)
        with io.open('debug_results/debug.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
    else:
        with open('debug_results/debug.json') as f:
            result = json.load(f)

    return filter_json_by_keyword(result, keyword)

def filter_json_by_keyword(json_data, keyword):
    if not keyword:
        return map_json_data(json_data)
    
    only_words_array = map_json_data(json_data)
    filtered_results = []
    for word in only_words_array:
        if remove_special_chars_and_accents(keyword) in remove_special_chars_and_accents(word["text"]):
            filtered_results.append(word)

    return filtered_results

def map_json_data(json_data):
    mapped_array = []
    for segment in json_data["segments"]:
        for word in segment["words"]:
          mapped_array.append(word)

    return mapped_array