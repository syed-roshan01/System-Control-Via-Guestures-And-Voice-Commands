import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
import numpy as np

# Initialize Mediapipe and mouse controller
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mouse = Controller()

# Constants for eye landmarks
LEFT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]

# Blink detection threshold
BLINK_RATIO_THRESHOLD = 5.0

# Webcam dimensions
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Cursor movement speed
CURSOR_SPEED = 20

# Helper function to calculate the blink ratio
def calculate_blink_ratio(eye_landmarks, landmarks):
    horizontal = np.linalg.norm(
        np.array([landmarks[eye_landmarks[0]].x, landmarks[eye_landmarks[0]].y]) -
        np.array([landmarks[eye_landmarks[3]].x, landmarks[eye_landmarks[3]].y])
    )
    vertical = np.linalg.norm(
        np.array([landmarks[eye_landmarks[1]].x, landmarks[eye_landmarks[1]].y]) -
        np.array([landmarks[eye_landmarks[5]].x, landmarks[eye_landmarks[5]].y])
    )
    return horizontal / vertical if vertical != 0 else 0

# Helper function to draw eye bounding boxes
def draw_eye_boxes(frame, eye_landmarks, landmarks):
    h, w, _ = frame.shape
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_landmarks]
    for point in points:
        cv2.circle(frame, point, 2, (0, 255, 0), -1)
    return points

# Start video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame for a mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            # Draw eye boxes and calculate blink ratios
            left_eye_points = draw_eye_boxes(frame, LEFT_EYE_LANDMARKS, landmarks)
            right_eye_points = draw_eye_boxes(frame, RIGHT_EYE_LANDMARKS, landmarks)

            left_blink_ratio = calculate_blink_ratio(LEFT_EYE_LANDMARKS, landmarks)
            right_blink_ratio = calculate_blink_ratio(RIGHT_EYE_LANDMARKS, landmarks)

            # Detect blinks for mouse clicks
            if left_blink_ratio > BLINK_RATIO_THRESHOLD:
                mouse.click(Button.left)
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if right_blink_ratio > BLINK_RATIO_THRESHOLD:
                mouse.click(Button.right)
                cv2.putText(frame, "Right Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Calculate average eye positions for cursor movement
            avg_x = np.mean([p[0] for p in left_eye_points + right_eye_points])
            avg_y = np.mean([p[1] for p in left_eye_points + right_eye_points])

            # Normalize and move the cursor
            norm_x = (avg_x - CAM_WIDTH / 2) / (CAM_WIDTH / 2)
            norm_y = (avg_y - CAM_HEIGHT / 2) / (CAM_HEIGHT / 2)
            mouse.move(norm_x * CURSOR_SPEED, norm_y * CURSOR_SPEED)

        # Display the frame
        cv2.imshow("Eye Gesture Control", frame)

        # Break on 'ESC' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
