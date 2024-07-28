import mediapipe as mp

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

def is_thumb_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    if thumb_tip.y < thumb_ip.y < thumb_mcp.y and thumb_mcp.y < index_finger_mcp.y:
        return True
    return False

def is_hand_open(hand_landmarks):
    extended_fingers = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                        mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, 
                        mp_hands.HandLandmark.PINKY_TIP]
    for finger_tip in extended_fingers:
        if hand_landmarks.landmark[finger_tip].y > hand_landmarks.landmark[finger_tip - 2].y:
            return False
    return True

def is_fist(hand_landmarks):
    folded_fingers = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                      mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, 
                      mp_hands.HandLandmark.PINKY_TIP]
    for finger_tip in folded_fingers:
        if hand_landmarks.landmark[finger_tip].y < hand_landmarks.landmark[finger_tip - 2].y:
            return False
    return True

def is_hands_above_head(pose_landmarks):
    left_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    head_top = pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y

    return (left_hand.y < head_top and right_hand.y < head_top)

def is_peace_sign(hand_landmarks):
    if (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y):
        return True
    return False

def is_ok_sign(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    
    if (thumb_tip.x < index_finger_tip.x and
        thumb_tip.y > index_finger_tip.y and
        thumb_ip.x < index_finger_dip.x):
        return True
    return False

def is_rock_sign(hand_landmarks):
    if (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y):
        return True
    return False

def is_y_pose(pose_landmarks):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    return (left_hand.y < left_shoulder.y and right_hand.y < right_shoulder.y and
            left_hand.x < left_shoulder.x and right_hand.x > right_shoulder.x)

def is_arms_crossed(pose_landmarks):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]


    left_hand_near_right_shoulder = abs(left_wrist.x - right_shoulder.x) < threshold and abs(left_wrist.y - right_shoulder.y) < threshold
    right_hand_near_left_shoulder = abs(right_wrist.x - left_shoulder.x) < threshold and abs(right_wrist.y - left_shoulder.y) < threshold

    return left_hand_near_right_shoulder and right_hand_near_left_shoulder

def is_one_hand_raised(pose_landmarks):
    if not pose_landmarks:
        return False

    left_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_hand_raised = left_hand.y < left_shoulder.y
    right_hand_raised = right_hand.y < right_shoulder.y

    return left_hand_raised or right_hand_raised