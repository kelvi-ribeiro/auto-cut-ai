
import utils.string_utils as string_utils

def filter_json_by_keyword(json_data, keyword):
    if not keyword:
        return map_json_data(json_data)
    
    only_words_array = map_json_data(json_data)
    filtered_results = []
    for word in only_words_array:
        if string_utils.remove_special_chars_and_accents(keyword) in string_utils.remove_special_chars_and_accents(word["text"]):
            filtered_results.append(word)

    return filtered_results

def map_json_data(json_data):
    mapped_array = []
    for segment in json_data["segments"]:
        for word in segment["words"]:
          mapped_array.append(word)

    return mapped_array