from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import os
import multiprocessing

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
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return None  
    cut_segments = cut_video(video, times_of_each_keyword_spoken, seconds_to_cut)
    if not cut_segments:
        print("No cuts found for the word passed")
    else:
        combined_video = concatenate_videoclips(cut_segments) 
        output_path = "export/" + os.path.basename(video_path) 
        combined_video.write_videofile(output_path, threads=multiprocessing.cpu_count())
        video.close()