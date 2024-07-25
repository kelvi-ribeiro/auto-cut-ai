import cv2
import mediapipe as mp
import numpy as np
from moviepy.editor import VideoFileClip

# Inicializando a MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

def is_hand_open(hand_landmarks):
    # Verificar se a mão está aberta com base nas posições dos pontos
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    
    # Verificar se todos os dedos estão afastados do pulso
    return all(finger_tip.y < wrist.y for finger_tip in [thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip])



def get_times_of_each_keyword_spoken(config, combined_videos):
    cap = cv2.VideoCapture(combined_videos.filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    times_of_each_keyword_spoken = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if is_hand_open(hand_landmarks):
                    seconds = frame_count / fps
                    print(f"Mão aberta detectada no segundo: {seconds:.2f}")                        
                    times_of_each_keyword_spoken.append({
                        'start': seconds - config["seconds_to_cut"],
                        'end': seconds + 4,
                        'cuts_count': 1
                        }) 
                    break
                 
    cap.release()
    return times_of_each_keyword_spoken
