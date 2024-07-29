from utils.file_utils import get_filename_from_full_path

class RecognitionProcessor:
    def __init__(self, files, config):
        self.files = files
        self.videos_duration = []
        self.times_of_each_cut = []
        self.config = config

    def process(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def print_process_status(self, idx, file):
        print(f"Processing '{idx + 1}/{len(self.files)}'. Video: '{get_filename_from_full_path(file)}'.")

    def add_time_cut(self, seconds_considered_same_gesture, seconds):
        last_index = len(self.times_of_each_cut) - 1
        start_time = seconds - self.config['seconds_to_cut']
        end = seconds
        if start_time == end:
            end = seconds + 1
        if last_index >= 0 and (seconds - self.times_of_each_cut[last_index]['end']) <= seconds_considered_same_gesture:
            self.times_of_each_cut[last_index]['end'] = seconds
        else:
            self.times_of_each_cut.append({
                                    'start': start_time,
                                    'end': seconds,
                                    'cuts_count': 1
                                })
    def get_times_cut_with_removed_duplicates(self):
        unique_list = []
        for times_of_each_cut in self.times_of_each_cut:
            unique_list_last_index = len(unique_list) - 1
            if(unique_list_last_index > 1 and unique_list[unique_list_last_index]['end'] > times_of_each_cut['start']):
                unique_list[unique_list_last_index]['end'] = times_of_each_cut['end'] 
                unique_list[unique_list_last_index]['merged'] = True
                unique_list[unique_list_last_index]['cuts_count'] += 1
            else:     
                times_of_each_cut['cuts_count'] = 1
                unique_list.append(times_of_each_cut)
        return unique_list
