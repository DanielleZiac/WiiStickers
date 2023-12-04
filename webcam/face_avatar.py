import cv2
import dlib
from imutils import face_utils

# Load the pre-trained face and landmark detector from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize OpenCV video capture
video_capture = cv2.VideoCapture(0)

# Load images for avatar
eyes_opened_image = cv2.imread("gui/avatar/eyesopened.png")
eyes_closed_image = cv2.imread("gui/avatar/eyesclosed.png")
mouth_opened_image = cv2.imread("gui/avatar/mouthopened.png")
mouth_closed_image = cv2.imread("gui/avatar/mouthclosed.png")

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

        left_eye_distance = shape[47][1] - shape[43][1]
        right_eye_distance = shape[41][1] - shape[37][1]

        left_eye_status = "Closed" if left_eye_distance < 15 else "Open"
        right_eye_status = "Closed" if right_eye_distance < 15 else "Open"

        # Check if mouth is open
        mouth_status = "Open" if shape[66][1] - shape[62][1] > 10 else "Closed"

        # Display the status and distances on the frame
        cv2.putText(frame, f"Left Eye: {left_eye_status} ({left_eye_distance})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Eye: {right_eye_status} ({right_eye_distance})", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Mouth: {mouth_status}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display corresponding avatar images
        if left_eye_status == "Open" and right_eye_status == "Open":
            cv2.imshow('Avatar Eyes', eyes_opened_image)
        else:
            cv2.imshow('Avatar Eyes', eyes_closed_image)

        if mouth_status == "Open":
            cv2.imshow('Avatar Mouth', mouth_opened_image)
        else:
            cv2.imshow('Avatar Mouth', mouth_closed_image)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
