import cv2
import dlib
from imutils import face_utils

# Load the pre-trained face and landmark detector from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

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

        # Extract coordinates for eyes and mouth
        left_eye = shape[2:4]  # Use points 2 and 3 for left eye
        right_eye = shape[0:2]  # Use points 0 and 1 for right eye
        mouth = shape[4]  # Use point 4 for the mouth

        # Draw the eyes and mouth on the frame
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        cv2.circle(frame, (mouth[0], mouth[1]), 2, (0, 255, 0), -1)

        # Check if eyes are open
        left_eye_status = "Open" if left_eye[1, 1] < left_eye[0, 0] else "Closed"
        right_eye_status = "Open" if right_eye[1, 1] < right_eye[0, 0] else "Closed"

        # Check if mouth is open
        mouth_status = "Open" if mouth[1] - mouth[0] > 10 else "Closed"

        # Display the status on the frame
        cv2.putText(frame, f"Left Eye: {left_eye_status}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Eye: {right_eye_status}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Mouth: {mouth_status}", (10, 90),
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