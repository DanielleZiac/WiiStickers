import cv2
import dlib
import numpy as np
from imutils import face_utils

# Load the pre-trained face and landmark detector from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize OpenCV video capture
video_capture = cv2.VideoCapture(0)

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

        # Extract coordinates for eyes
        left_eye = shape[42:48]
        right_eye = shape[36:42]

        # Define the region of interest (ROI) below the face
        roi_shirt = frame[face.bottom():, face.left():face.right()]

        # Calculate the average color of the shirt region
        avg_color = np.mean(roi_shirt, axis=(0, 1))

        # Convert the color to the HSV color space
        avg_color_hsv = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_BGR2HSV)[0][0]

        # Draw a box around the detected face
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)

        # Display the detected color in a box
        cv2.rectangle(frame, (face.left(), face.bottom()), (face.right(), frame.shape[0]), avg_color, -1)

        # Display the detected color in HSV
        cv2.putText(frame, f"Detected Color (HSV): {avg_color_hsv}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
