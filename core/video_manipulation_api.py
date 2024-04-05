from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

def cut_video(video, cuts, seconds_to_cut):
    cut_segments = []
    for cut in cuts:
        start_time = (cut.get("end") - seconds_to_cut)
        end_time = cut.get("end")

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
    combined_video = concatenate_videoclips(cut_segments) # TODO TRATAR VAZIO
    output_path = "export/" +  video_path + '_exported.mp4'
    combined_video.write_videofile(output_path)
    video.close()