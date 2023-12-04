import cv2
import dlib
import numpy as np
from imutils import face_utils

# Load the pre-trained face and landmark detector from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize OpenCV video capture
video_capture = cv2.VideoCapture(0)

# Set the region for color detection (bottom center)
rect_x, rect_y, rect_width, rect_height = 600, 600, 100, 50

# Initialize variables to store color information
detected_color = (0, 0, 0)

# Convert the detected_color tuple to a list of integers
color_list = [int(component) for component in detected_color]

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Extract coordinates for eyes and mouth
        left_eye = shape[42:48]
        right_eye = shape[36:42]
        mouth = shape[48:68]

        # Draw the eyes and mouth on the frame
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in mouth:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        left_eye_distance = shape[47][1] - shape[43][1]
        right_eye_distance = shape[41][1] - shape[37][1]

        left_eye_status = "Closed" if left_eye_distance < 15 else "Open"
        right_eye_status = "Closed" if right_eye_distance < 15 else "Open"

        eyes_status = "Closed" if left_eye_distance < 15 and right_eye_distance < 15 else "Open"

        # Check if mouth is open
        mouth_status = "Open" if shape[66][1] - shape[62][1] > 10 else "Closed"

        roi = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]

        # Calculate the average color in the ROI
        avg_color = np.mean(roi, axis=(0, 1)).astype(int)

        # Convert the average color to tuple
        detected_color = tuple(map(int, avg_color))

        # Display the region for color detection
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

        # Display the detected color and its values in a box on the top right corner
        cv2.rectangle(frame, (10, 300), (200, 200), detected_color, -1)
        cv2.putText(frame, f"Color: {detected_color}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


        # Display the status and distances on the frame
        cv2.putText(frame, f"Left Eye: {left_eye_status} ({left_eye_distance})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Eye: {right_eye_status} ({right_eye_distance})", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Both Eyes: {eyes_status}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Mouth: {mouth_status}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face and Shirt Color Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()