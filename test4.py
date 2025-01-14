import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize mediapipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Capture webcam video
cap = cv2.VideoCapture(0)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Flag to track if left click is in progress
click_in_progress = False
right_click_in_progress = False

def detect_zooming(hand_landmarks):
    window = 0.03

    # Check if index and middle fingers are up, and other fingers are down
    index_up = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < \
               hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_up = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < \
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_down = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > \
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    little_down = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > \
                  hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    zooming = index_up and middle_up and ring_down and little_down

    # Calculate the horizontal distance between the index and middle fingertips
    index_touches_middle = abs(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x - \
                               hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x) <= window

    zooming_out = zooming and index_touches_middle
    zooming_in = zooming and not index_touches_middle

    if zooming_out:
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(-100)  # Faster zoom out
        pyautogui.keyUp('ctrl')
        print("Zooming Out")

    if zooming_in:
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(100)  # Faster zoom in
        pyautogui.keyUp('ctrl')
        print("Zooming In")

def detect_left_click(hand_landmarks):
    global click_in_progress

    # Check if thumb tip and index finger tip are close to each other
    window = 0.03
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    distance = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)

    if distance < window and not click_in_progress:
        pyautogui.click()
        click_in_progress = True
        print("Left Click")
    elif distance >= window:
        click_in_progress = False


def detect_right_click(hand_landmarks):
    global right_click_in_progress

    # Check if thumb tip and middle finger tip are close to each other
    window = 0.03
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    distance = math.sqrt((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2)

    if distance < window and not right_click_in_progress:
        pyautogui.rightClick()
        right_click_in_progress = True
        print("Right Click")
    elif distance >= window:
        right_click_in_progress = False

def move_cursor_with_palm(hand_landmarks, frame_width, frame_height, screen_width, screen_height):
    # Check if all fingers are up (extended) to ensure the hand is open
    all_fingers_up = (
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    )

    if not all_fingers_up:
        return  # Don't move the cursor if fingers are not open

    # Calculate the palm center (average of all landmark positions)
    palm_x = 0
    palm_y = 0

    # Palm landmarks: wrist (landmark 0), and the four finger bases (landmarks 1, 5, 9, 13, 17)
    palm_landmarks = [hand_landmarks.landmark[i] for i in [0, 1, 5, 9, 13, 17]]
    for landmark in palm_landmarks:
        palm_x += landmark.x
        palm_y += landmark.y

    # Calculate the center of the palm
    palm_x /= len(palm_landmarks)
    palm_y /= len(palm_landmarks)

    # Map palm center to screen coordinates
    screen_x = int(palm_x * screen_width)
    screen_y = int(palm_y * screen_height)

    # Move the mouse cursor if a click is not in progress
    if not click_in_progress and not right_click_in_progress:
        pyautogui.moveTo(screen_x, screen_y)

def draw_green_circles_for_raised_fingers(hand_landmarks, frame):
    # Check if each finger is raised (tip above the PIP joint)
    index_raised = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_raised = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < \
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_raised = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < \
                  hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_raised = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    # Draw green circle for each raised finger
    if index_raised:
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index_tip.x * frame.shape[1])
        y = int(index_tip.y * frame.shape[0])
        cv2.circle(frame, (x, y), 6 , (0, 255, 0), -1)

    if middle_raised:
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        mx = int(middle_tip.x * frame.shape[1])
        my = int(middle_tip.y * frame.shape[0])
        cv2.circle(frame, (mx, my), 6 , (0, 255, 0), -1)

    if ring_raised:
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        rx = int(ring_tip.x * frame.shape[1])
        ry = int(ring_tip.y * frame.shape[0])
        cv2.circle(frame, (rx, ry), 6 , (0, 255, 0), -1)

    if pinky_raised:
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        px = int(pinky_tip.x * frame.shape[1])
        py = int(pinky_tip.y * frame.shape[0])
        cv2.circle(frame, (px, py), 6 , (0, 255, 0), -1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert the frame to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Process hand landmarks if any are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame (for debugging purposes, remove if not needed)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect zooming gestures
            detect_zooming(hand_landmarks)

            # Detect left click gesture
            detect_left_click(hand_landmarks)

            # Detect right click gesture
            detect_right_click(hand_landmarks)

            # Move the cursor based on the palm center
            move_cursor_with_palm(hand_landmarks, frame_width, frame_height, screen_width, screen_height)

            # Draw green circles for raised fingers
            draw_green_circles_for_raised_fingers(hand_landmarks, frame)

    # Display the video feed
    cv2.imshow("Hand Gesture Cursor Control", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
