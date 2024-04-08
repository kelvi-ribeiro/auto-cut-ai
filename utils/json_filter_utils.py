
import utils.string_utils as string_utils
import json

def filter_json_by_keyword(times_of_each_keyword_spoken, keyword, seconds_to_cut):
    filtered_results = []
    print(f"About to map the '{keyword}' in result" )
    with open('config.json') as config_file:
            config = json.load(config_file)
    for word in times_of_each_keyword_spoken: 
        if string_utils.remove_special_chars_and_accents(keyword) in string_utils.remove_special_chars_and_accents(word["text"]) and word["confidence"] > config["minimum_confidence"]:
            filtered_results_last_index = len(filtered_results) - 1
            if(filtered_results_last_index > 1 and (word["end"] - seconds_to_cut) < filtered_results[filtered_results_last_index]["end"]):
                print(f"{word}' with duplicated timeline, about to merge into {filtered_results[filtered_results_last_index]}")
                filtered_results[filtered_results_last_index]["end"] = word["end"]
                print(f"timestamp {filtered_results[filtered_results_last_index]}' after merge")
            else:     
                print(f"{word}' found in array, about to add in filtered_results")
                filtered_results.append(word)

    return filtered_results