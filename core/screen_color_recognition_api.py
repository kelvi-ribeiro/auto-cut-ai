import cv2
from utils.file_utils import get_filename_from_full_path

def get_times_of_each_cut(config, files):
    threshold=10
    times_of_each_cut = []
    videos_duration = []
    for idx, file in enumerate(files):
        print(f"Gesture processing '{idx + 1}/{len(files)}'. Video: '{get_filename_from_full_path(file)}'.")
        cap = cv2.VideoCapture(file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        seconds_considered_same_gesture = 4
        frame_interval = int(fps)  
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_video_duration = frame_count / fps
        while cap.isOpened():
            frame_position = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if (frame_position / fps) > current_video_duration:
                break

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position + frame_interval)
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if cv2.mean(gray_frame)[0] < threshold:
                seconds = (frame_position / fps) 
                if idx > 0 :
                    seconds += sum(videos_duration)
                print(f"Black screen detected in {seconds:.2f} seconds")
                last_index = len(times_of_each_cut) - 1                         
                if last_index >= 0 and (seconds - times_of_each_cut[last_index]['end']) <= seconds_considered_same_gesture:
                    times_of_each_cut[last_index]['end'] = seconds
                else: 
                    times_of_each_cut.append({
                        'start': seconds - config['seconds_to_cut'],
                        'end': seconds + 1,
                        'cuts_count': 1
                    })

            
        videos_duration.append(current_video_duration)
        cap.release()
    return times_of_each_cut
