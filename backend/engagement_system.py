import warnings
warnings.filterwarnings("ignore", category=UserWarning, message='SymbolDatabase.GetPrototype() is deprecated. Please ')

import cv2
import mediapipe as mp
import numpy as np
import time
from scipy.spatial import distance as dist
import csv
import os
from datetime import datetime, timedelta

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Drawing specifications
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Capture video
cap = cv2.VideoCapture(0)

# Helper function to draw text with a background
def draw_text_with_background(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.8, font_thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    x, y = position
    cv2.rectangle(image, (x, y - text_h - 10), (x + text_w + 10, y + 10), bg_color, -1)
    cv2.putText(image, text, (x, y), font, font_scale, text_color, font_thickness)

# Engagement monitoring variables
engagement_score = 100  # Starting engagement score
attention_threshold = 3  # Time threshold for inattention in seconds
inattention_start_time = None
total_inattention_duration = 0  # Total time user was not engaging
no_face_start_time = None  # Time when no face was detected
total_no_face_duration = 0  # Total time no face was detected

# EAR calculation function
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Indices for the left and right eye landmarks
LEFT_EYE = [362, 385, 387, 263, 373, 380, 382, 381, 384, 398]
RIGHT_EYE = [33, 160, 158, 133, 153, 144, 157, 173, 163, 165]

# Define EAR threshold
EYE_THRESHOLD = 0.25

# Initialize head_text
head_text = "Forward"

# Define CSV filename (single file for all data)
directory = "engagement_data"
if not os.path.exists(directory):
    os.makedirs(directory)
filename = os.path.join(directory, 'engagement_data.csv')

# Check if the file already exists
file_exists = os.path.isfile(filename)

# Open the CSV file in append mode and initialize writer
csv_file = open(filename, mode='a', newline='')
fieldnames = ['date', 'runtime', 'timestamp', 'engagement_score', 'inattention_duration', 'no_face_duration']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

# Write header only if the file is new
if not file_exists:
    writer.writeheader()

# Track start time to calculate runtime
start_time = time.time()


# Smoothing function for landmarks
def smooth_landmarks(landmarks, smoothing_factor=5):
    smoothed_landmarks = []
    for i in range(len(landmarks)):
        start_idx = max(0, i - smoothing_factor)
        end_idx = min(len(landmarks), i + smoothing_factor + 1)
        smoothed_landmarks.append(np.mean(landmarks[start_idx:end_idx], axis=0))
    return smoothed_landmarks

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    start = time.time()

    # Flip the image horizontally for a later selfie-view display
    # Convert the color space from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False

    # Get the result from face mesh
    results = face_mesh.process(image)

    # Convert the color space from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        no_face_start_time = None  # Reset no face detection timer

        for face_landmarks in results.multi_face_landmarks:
            # Draw the face mesh on the image
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )
            landmarks = face_landmarks.landmark
            left_eye = np.array([(landmarks[i].x * img_w, landmarks[i].y * img_h) for i in LEFT_EYE], dtype=np.float64)
            right_eye = np.array([(landmarks[i].x * img_w, landmarks[i].y * img_h) for i in RIGHT_EYE], dtype=np.float64)

            left_eye = smooth_landmarks(left_eye)
            right_eye = smooth_landmarks(right_eye)

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            # Determine gaze direction based on EAR and head tilt
            if ear < EYE_THRESHOLD:
                gaze_text = "Blinking"
            elif head_text != "Forward":
                gaze_text = "Looking away"
            else:
                gaze_text = "Looking center"

            draw_text_with_background(image, gaze_text, (20, 30))
            draw_text_with_background(image, f'EAR: {ear:.2f}', (20, 70))

            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])

            # Ensure there are enough points
            if len(face_2d) >= 4:
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = img_w
                cam_matrix = np.array([[focal_length, 0, img_w / 2],
                                       [0, focal_length, img_h / 2],
                                       [0, 0, 1]])

                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                # See where the user's head is tilting
                if y < -10:
                    head_text = "Looking Left"
                    if inattention_start_time is None:
                        inattention_start_time = time.time()
                elif y > 10:
                    head_text = "Looking Right"
                    if inattention_start_time is None:
                        inattention_start_time = time.time()
                elif x < -10:
                    head_text = "Looking Down"
                    if inattention_start_time is None:
                        inattention_start_time = time.time()
                elif x > 10:
                    head_text = "Looking Up"
                    if inattention_start_time is None:
                        inattention_start_time = time.time()
                else:
                    head_text = "Forward"
                    inattention_start_time = None  # Reset inattention start time if looking forward

                # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                # Add the text on the image
                draw_text_with_background(image, head_text, (20, 110))
                # draw_text_with_background(image, "X: " + str(np.round(x, 2)), (20, 150))
                # draw_text_with_background(image, "Y: " + str(np.round(y, 2)), (20, 190))
                # draw_text_with_background(image, "Z: " + str(np.round(z, 2)), (20, 230))

        # Inattention handling
        if inattention_start_time:
            inattention_duration = time.time() - inattention_start_time
            draw_text_with_background(image, f'Inattention Duration: {inattention_duration:.2f}s', (20, 270))

            # If the inattention duration exceeds the threshold, decrement the engagement score
            if inattention_duration > attention_threshold:
                engagement_score -= 1
                inattention_start_time = None  # Reset inattention start time after decrementing score
                total_inattention_duration += inattention_duration  # Accumulate total inattention duration

                # Calculate the runtime
                runtime = time.time() - start_time
                current_date = datetime.now().strftime('%Y-%m-%d')

                # Replace the existing timestamp entry with a human-readable format
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Replace the existing inattention_duration entry with a human-readable format
                human_readable_inattention_duration = str(timedelta(seconds=int(total_inattention_duration)))
                human_readable_no_face_duration = str(timedelta(seconds=int(total_no_face_duration)))

                # Log important engagement data to CSV
                writer.writerow({
                    'date': current_date,
                    'runtime': f'{runtime:.2f}s',
                    'timestamp': current_time,
                    'engagement_score': engagement_score,
                    'inattention_duration': human_readable_inattention_duration,
                    'no_face_duration': human_readable_no_face_duration
                })
                csv_file.flush()  # Ensure data is written immediately

    else:
        # No face detected
        if no_face_start_time is None:
            no_face_start_time = time.time()
        no_face_duration = time.time() - no_face_start_time

        draw_text_with_background(image, f'No User Detected: {no_face_duration:.2f}s', (20, 310))

        # If no face is detected for more than a threshold, consider it as absence
        if no_face_duration > attention_threshold:
            engagement_score -= 1
            no_face_start_time = None  # Reset no face start time after decrementing score
            total_no_face_duration += no_face_duration

            # Calculate the runtime
            runtime = time.time() - start_time
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Replace the existing timestamp entry with a human-readable format
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Replace the existing inattention_duration entry with a human-readable format
            human_readable_inattention_duration = str(timedelta(seconds=int(total_inattention_duration)))
            human_readable_no_face_duration = str(timedelta(seconds=int(total_no_face_duration)))

                # Log important engagement data to CSV
            writer.writerow({
                    'date': current_date,
                    'runtime': f'{runtime:.2f}s',
                    'timestamp': current_time,
                    'engagement_score': engagement_score,
                    'inattention_duration': human_readable_inattention_duration,
                    'no_face_duration': human_readable_no_face_duration
                })
            csv_file.flush()  # Ensure data is written immediately


    # Update engagement score on the image
    draw_text_with_background(image, f'Engagement Score: {engagement_score}', (20, 350))
    draw_text_with_background(image, f'Total Inattention Duration: {total_inattention_duration:.2f}s', (20, 390))
    draw_text_with_background(image, f'Total No Face Duration: {total_no_face_duration:.2f}s', (20, 430))

    end = time.time()
    totalTime = end - start

    # # Prevent division by zero
    # if totalTime > 0:
    #     fps = 1 / totalTime
    #     draw_text_with_background(image, f'FPS: {fps:.2f}', (20, 470))

    # Display the image
    cv2.imshow('Head Pose Estimation', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()