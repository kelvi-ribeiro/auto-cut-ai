
import utils.string_utils as string_utils
import utils.debug_utils as debug_utils
import json

def extract_keyword_occurrences(times_of_each_keyword_spoken, keyword): 
    filtered_results = []
    print(f"About to map the '{keyword}' in result" )
    with open('config.json') as config_file:
            config = json.load(config_file)
    for word in times_of_each_keyword_spoken: 
        if string_utils.remove_special_chars_and_accents(keyword) in string_utils.remove_special_chars_and_accents(word['text']) and word['confidence'] > config['minimum_confidence']:
            filtered_results_last_index = len(filtered_results) - 1
            if(filtered_results_last_index > 1 and filtered_results[filtered_results_last_index]['end'] > word['start']):
                print(f"{word}' with duplicated timeline, about to merge into {filtered_results[filtered_results_last_index]}")
                filtered_results[filtered_results_last_index]['end'] = word['end'] 
                filtered_results[filtered_results_last_index]['merged'] = True
                filtered_results[filtered_results_last_index]['cuts_count'] += 1
                print(f"timestamp {filtered_results[filtered_results_last_index]}' after merge")
            else:     
                print(f"{word}' found in array, about to add in filtered_results")
                word['cuts_count'] = 1
                filtered_results.append(word)

    debug_utils.save_debug_file(filtered_results, config['final_video_name'] + "_filtered")
    return filtered_results