import cv2
from core.recognition_processor import RecognitionProcessor

class BlinkScreenRecognition(RecognitionProcessor):
    def __init__(self, files, config, notification_system):
        super().__init__(files, config, notification_system)

    def process(self):
        threshold=40
        for idx, file in enumerate(self.files):
            self.print_process_status(idx, file)
            self.update_progress_bar("Buscando por piscadas no vídeo", idx) 
            cap = cv2.VideoCapture(file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            seconds_considered_same_gesture = 4
            frame_interval = int(fps / 2)  
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
                        seconds += sum(self.videos_duration)
                    self.notification_system.notify(f"Corte detectado em {seconds:.2f} segundos.")
                    self.add_time_cut(seconds, seconds_considered_same_gesture)

                
            self.videos_duration.append(current_video_duration)
            cap.release()
        return self.get_times_cut_with_removed_duplicates()
