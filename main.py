import whisper_integration as whis;
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoClip, concatenate_videoclips
 

def cut_video(video_path, cuts, seconds_to_cut):
    try:
        # Load the video using MoviePy
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return None  # Return None if video loading fails

    # List to store the cut segments
    cut_segments = []

    # Loop through the start and end times to perform the cuts
    for cut in cuts:
        start_time = (cut.get("end") - seconds_to_cut)
        end_time = cut.get("end")

        # Check if start and end times are within video duration
        if 0 <= start_time <= video.duration and 0 <= end_time <= video.duration:
            # Cut the video within the specified interval
            segment = video.subclip(start_time, end_time)
            # Append the cut segment to the list
            cut_segments.append(segment)
        else:
            print(f"Ignoring invalid cut: {cut}")

    # Close the original video
    #video.close() TODO COLOCAR PRA FECHAR NO MÉTODO QUE CHAMA

    # Return the list of cut segments
    return cut_segments


filePath = "Video_Falado.mp4"
result = whis.get_json_timestamped_result("manga", filePath)

# Call the method to perform the cuts on the video
cut_segments = cut_video(filePath, result, 3)

# Combine the cut segments into a single video
combined_video = concatenate_videoclips(cut_segments) # TRATAR VAZIO

# Save the combined video to the root path
output_path = 'final_video.mp4'
combined_video.write_videofile(output_path)