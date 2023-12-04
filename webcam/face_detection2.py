import cv2
import matplotlib.pyplot as plt
import dlib
from imutils import face_utils

font= cv2.FONT_HERSHEY_SIMPLEX

cascPath = "./envlib/python3.12/site-packages/cv2/data/haarcascade_frontalface_default.xml"
eyePath = "./env/lib/python3.12/site-packages/cv2/data/haarcascade_eye.xml"
smilePath = "./env/lib/python3.12/site-packages/cv2/data/haarcascade_smile.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)
smileCascade = cv2.CascadeClassifier(smilePath)

dnnFaceDetector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

video_capture = cv2.VideoCapture(1)
flag = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = dnnFaceDetector(gray, 1)

    for (i, rect) in enumerate(rects):

        x1 = rect.rect.left()
        y1 = rect.rect.top()
        x2 = rect.rect.right()
        y2 = rect.rect.bottom()

        # Rectangle around the face
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the video output
    cv2.imshow('Video', frame)

    # Quit video by typing Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()