from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
from utils.file_utils import get_filename_from_full_path
import multiprocessing
import pathlib

def cut_video(video, cuts):
    cut_segments = []
    for cut in cuts:
        start_time = cut.get("start")
        end_time = cut.get("end")
        if start_time < 0: 
            start_time = 0
        if end_time > video.duration:
            end_time = video.duration
            
        segment = video.subclip(start_time, end_time)
        cut_segments.append(segment)

    return cut_segments

def generate_video(video_path, times_of_each_keyword_spoken, dir_to_save):
    cut_segments = []
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return None  
    cut_segments = cut_video(video, times_of_each_keyword_spoken)
    if not cut_segments:
        print("No cuts found for the word passed")
    else:
        print(f"'{len(cut_segments)}' cuts were found in the video '{video_path}'")
        combined_video = concatenate_videoclips(cut_segments) 
        combined_video.write_videofile(dir_to_save + "/" + get_filename_from_full_path(video_path), threads=multiprocessing.cpu_count())
        video.close()
    return (len(cut_segments), sum(i['end'] - i['start']   for i in times_of_each_keyword_spoken))

def merge_videos(videos_paths, final_video_name, dir_to_save):
    print(f"About to merge '{len(videos_paths)}' videos")
    videos = []
    for video_path in videos_paths:
        try:
            videos.append(VideoFileClip(video_path)) 
        except Exception as e:
            print(f"Error loading video: {e}")
            return None  
    combined_videos = concatenate_videoclips(videos) 
    output_path = dir_to_save + "/" + final_video_name  + pathlib.Path(videos_paths[0]).suffix 
    combined_videos.write_videofile(output_path, threads=multiprocessing.cpu_count())
    for video in videos:
        video.close()
    return output_path