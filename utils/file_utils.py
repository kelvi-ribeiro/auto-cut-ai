import os
import io, json
from utils.constants import SAVED_RESULT_PATH
import os

def get_pathname_without_extension(full_path):
    pathname, _ = os.path.splitext(full_path)
    
    filename_without_extension = os.path.basename(pathname)
    
    return filename_without_extension

def get_filename_from_full_path(full_path):
    return os.path.basename(full_path)

def save_result_file(times_of_each_cut, final_video_name): 
     print("about to save the result_file")
     json_data = json.dumps(times_of_each_cut, indent=4, ensure_ascii=False)
     with io.open(get_result_file_name(final_video_name), 'w', encoding='utf-8') as f:
        f.write(json_data)

def get_result_file(final_video_name):
     with open(get_result_file_name(final_video_name), 'r', encoding='utf-8') as f:
         return json.load(f)

def get_result_file_name(final_video_name):
    return f'{SAVED_RESULT_PATH}{os.sep}{final_video_name}_result.json'
