
import utils.string_utils as string_utils
import json

def filter_json_by_keyword(times_of_each_keyword_spoken, keyword):
    filtered_results = []
    print(f"About to map the '{keyword}' in result" )
    with open('config.json') as config_file:
            config = json.load(config_file)
    for word in times_of_each_keyword_spoken: 
        if string_utils.remove_special_chars_and_accents(keyword) in string_utils.remove_special_chars_and_accents(word["text"]) and word["confidence"] > config["minimum_confidence"]:
            time_threshold = 3.0  
            if not any(word["end"] - obj["end"]  < time_threshold for obj in filtered_results):
                print(f"{word}' found in array")
                filtered_results.append(word)

    return filtered_results