import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

def is_peace_sign(hand_landmarks):
    if (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y):
        return True
    return False

def get_times_of_each_cut(config, files):
    times_of_each_cut = []
    videos_duration = []
    for idx, file in enumerate(files):
        print(f"Gesture processing of video '{file}'")
        cap = cv2.VideoCapture(file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        seconds_considered_same_gesture = 3
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
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if is_peace_sign(hand_landmarks):
                        seconds = (frame_position / fps) 
                        if idx > 0 :
                            seconds += sum(videos_duration)
                        
                        print(f"Gesture detected at second: '{seconds:.2f}'")
                        last_index = len(times_of_each_cut) - 1                         
                        if last_index >= 0 and (seconds - times_of_each_cut[last_index]['end']) <= seconds_considered_same_gesture:
                            times_of_each_cut[last_index]['end'] = seconds
                        else: 
                            times_of_each_cut.append({
                                'start': seconds, ## TODO ALTERAR TEMPO
                                'end': seconds + 1,
                                'cuts_count': 1
                            })
                        break  
        videos_duration.append(current_video_duration)
        cap.release()
    return times_of_each_cut
