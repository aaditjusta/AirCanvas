import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

# Get camera frame
ret, frame = cap.read()

if not ret:
    print("Could not open camera")
    cap.release()
    exit()

# Get exact camera dimensions
height, width, channels = frame.shape

# Create canvas with EXACT same dimensions
canvas = np.zeros((height, width, channels), dtype=np.uint8)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

prev_x = 0
prev_y = 0
color = (255, 0, 0)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera")
        break

    frame = cv2.flip(frame, 1)

    # Colour palette on right side
    cv2.rectangle(frame, (width - 150, 20), (width - 20, 120), (0, 0, 255), -1)
    cv2.rectangle(frame, (width - 150, 140), (width - 20, 240), (0, 255, 0), -1)
    cv2.rectangle(frame, (width - 150, 260), (width - 20, 360), (255, 0, 0), -1)

    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            landmarks = hand.landmark

            # Index fingertip
            index_x = int(landmarks[8].x * width)
            index_y = int(landmarks[8].y * height)

            # Draw line
            # Check which fingers are up
            index_up = landmarks[8].y < landmarks[6].y
            middle_up = landmarks[12].y < landmarks[10].y

            ring_up = landmarks[16].y < landmarks[14].y
            pinky_up = landmarks[20].y < landmarks[18].y

            palm_up = index_up and middle_up and ring_up and pinky_up

            if index_up and middle_up and not ring_up and not pinky_up:

                if width - 150 < index_x < width - 20 and 20 < index_y < 120:
                    color = (0, 0, 255)
                    print("RED")

                elif width - 150 < index_x < width - 20 and 140 < index_y < 240:
                    color = (0, 255, 0)
                    print("GREEN")

                elif width - 150 < index_x < width - 20 and 260 < index_y < 360:
                    color = (255, 0, 0)
                    print("BLUE")

                elif width - 150 < index_x < width - 20 and 380 < index_y < 480:
                    color = (0, 0, 0)
                    print("ERASER")

                prev_x = 0
                prev_y = 0
                

            # Draw only when index finger is up
            # and middle finger is down
            elif index_up and not middle_up:

                if prev_x != 0 and prev_y != 0:

                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (index_x, index_y),
                        color,
                        5
                    )

                prev_x = index_x
                prev_y = index_y

            elif palm_up:

                cv2.circle(
                    canvas,
                    (index_x, index_y),
                    70,
                    (0, 0, 0),
                    -1
                )

                prev_x = 0
                prev_y = 0

            else:

                # Reset previous position
                prev_x = 0
                prev_y = 0
                

            # Red dot on fingertip
            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (0, 0, 255),
                -1
            )

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    # Combine canvas and camera
    frame = cv2.add(frame, canvas)

    cv2.imshow("Virtual Painter", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()