import cv2
import mediapipe as mp
from utils.file_utils import get_filename_from_full_path
from core.gesture_recognition.hands_gestures import is_peace_sign
from core.recognition_processor import RecognitionProcessor

class GestureRecognition(RecognitionProcessor):
    def __init__(self, files, config, notification_system):
        super().__init__(files, config, notification_system)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5)

    def process(self):
        for idx, file in enumerate(self.files):
            self.print_process_status(idx, file)
            self.update_progress_bar("Buscando pelo gesto escolhido", idx) 
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

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if is_peace_sign(hand_landmarks):
                            seconds = (frame_position / fps)
                            if idx > 0:
                                seconds += sum(self.videos_duration)

                            self.notification_system.notify(f"Corte detectado em {seconds:.2f} segundos.")
                            self.add_time_cut(seconds, seconds_considered_same_gesture)
                            break
            self.videos_duration.append(current_video_duration)
            cap.release()
        return self.get_times_cut_with_removed_duplicates()
