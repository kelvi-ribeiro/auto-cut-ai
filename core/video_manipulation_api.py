from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import os

def cut_video(video, cuts, seconds_to_cut):
    cut_segments = []
    for cut in cuts:
        start_time = (cut.get("start") - seconds_to_cut)
        end_time = cut.get("end")
        ## TODO Tratar de forma melhor, se start for maior que início do vídeo, pegar início do vídeo como referência
        ## TODO Se o final do vídeo for maior que a duração, pegar tempo de vuração como tempo final
        if 0 <= start_time <= video.duration and 0 <= end_time <= video.duration:
            segment = video.subclip(start_time, end_time)
            cut_segments.append(segment)
        else:
            print(f"Ignoring invalid cut: {cut}")
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
        combined_video.write_videofile(output_path)
        video.close()