import io, json
from utils.file_utils import get_pathname_without_extension

def save_debug_file(times_of_each_keyword_spoken, video_path): 
     print("about to save the debug_file")
     json_data = json.dumps(times_of_each_keyword_spoken, indent=4, ensure_ascii=False)
     with io.open(get_debug_file_name(video_path), 'w', encoding='utf-8') as f:
        f.write(json_data)

def get_debug_file(video_path):
     with open(get_debug_file_name(video_path)) as f:
         return json.load(f)

def get_debug_file_name(video_path):
    return f'debug/{get_pathname_without_extension(video_path)}_debug.json'