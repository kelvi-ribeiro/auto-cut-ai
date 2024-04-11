import io, json
from utils.file_utils import get_pathname_without_extension

def save_debug_file(times_of_each_keyword_spoken, final_video_name): 
     print("about to save the debug_file")
     json_data = json.dumps(times_of_each_keyword_spoken, indent=4, ensure_ascii=False)
     with io.open(get_debug_file_name(final_video_name), 'w', encoding='utf-8') as f:
        f.write(json_data)

def get_debug_file(final_video_name):
     with open(get_debug_file_name(final_video_name)) as f:
         return json.load(f)

def get_debug_file_name(final_video_name):
    return f'debug/{final_video_name}_debug.json'