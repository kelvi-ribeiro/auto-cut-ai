from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import multiprocessing
import os
from utils.constants import MIN_VIDEO_SECONDS

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
    return (cut_segments, sum(i['cuts_count'] for i in cuts))

def generate_video(combined_videos, times_of_each_cut, dir_to_save, config):
    cut_segments = []
    cut_segments, total_cuts = cut_video(combined_videos, times_of_each_cut)
    if not cut_segments:
        print("No cuts found")
    else:
        print(f"'{total_cuts}' cuts were found in the video '{config['final_video_name']}'")
        concatenated_videoclips = concatenate_videoclips(cut_segments) 
        if config['flip'] is True:
            concatenated_videoclips = concatenated_videoclips.add_mask().rotate(180)

        num_threads = max(1, multiprocessing.cpu_count() - 1)
        concatenated_videoclips.write_videofile(f"{dir_to_save}{os.sep}{config['final_video_name']}.mp4", threads=num_threads, preset='ultrafast')
    return (total_cuts, sum(i['end'] - i['start'] for i in times_of_each_cut))

def merge_videos(videos_paths):
    videos = []
    for video_path in videos_paths:
        try:
            video = VideoFileClip(video_path)
            if video.duration >= MIN_VIDEO_SECONDS:
                videos.append(VideoFileClip(video_path)) 
            else:
                print(f"Ignoring the video '{video_path}' with '{video.duration}' seconds because it is less than '{MIN_VIDEO_SECONDS}', the minimum allowed seconds")
        except Exception as e:
            print(f"Error loading video: {e}")
            return None  
    ## TODO DAR UM JEITO DE FECHAR OS VÍDEOS, TEM ALGUNS CASOS QUE DÁ ERRO NO FINAL DO PROCESSO
    ## video.close
    print(f"About to merge '{len(videos)}' videos")
    if(len(videos) == 1):  
        return videos[0]

    return concatenate_videoclips(videos) 