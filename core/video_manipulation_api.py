from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import os
import multiprocessing
from utils.constants import VIDEO_GENERATION_PATH, EXPORT_PATH
import pathlib

def cut_video(video, cuts, seconds_to_cut):
    cut_segments = []
    for cut in cuts:
        start_time = (cut.get("end") - seconds_to_cut)
        end_time = cut.get("end") + 1
        if start_time < 0: 
            start_time = 0
        if end_time > video.duration:
            end_time = video.duration
            
        segment = video.subclip(start_time, end_time)
        cut_segments.append(segment)

    return cut_segments

def generate_video(video_path, times_of_each_keyword_spoken, seconds_to_cut):
    cut_segments = []
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return None  
    cut_segments = cut_video(video, times_of_each_keyword_spoken, seconds_to_cut)
    if not cut_segments:
        print("No cuts found for the word passed")
    else:
        print(f"'{len(cut_segments)}' cuts were found to create a video in '{video_path}'")
        combined_video = concatenate_videoclips(cut_segments) 
        output_path = VIDEO_GENERATION_PATH + "/" + os.path.basename(video_path) 
        combined_video.write_videofile(output_path, threads=multiprocessing.cpu_count())
        video.close()
    return len(cut_segments)

def merge_videos(videos_paths, final_video_name):
    print(f"About to merge '{len(videos)}' videos")
    videos = []
    for video_path in videos_paths:
        try:
            videos.append(VideoFileClip(video_path)) 
        except Exception as e:
            print(f"Error loading video: {e}")
            return None  
    combined_videos = concatenate_videoclips(videos) 
    output_path = EXPORT_PATH + "/" + final_video_name + pathlib.Path(videos_paths[0]).suffix 
    combined_videos.write_videofile(output_path, threads=multiprocessing.cpu_count())
    for video in videos:
        video.close()