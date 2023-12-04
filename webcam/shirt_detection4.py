import cv2
import numpy as np

# Create a video capture object (0 corresponds to the default camera)
cap = cv2.VideoCapture(0)

# Set the region for color detection (bottom center)
rect_x, rect_y, rect_width, rect_height = 200, 400, 100, 50

# Initialize variables to store color information
detected_color = (0, 0, 0)

# Convert the detected_color tuple to a list of integers
color_list = [int(component) for component in detected_color]

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Extract the region of interest (ROI) for color detection
    roi = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]

    # Calculate the average color in the ROI
    avg_color = np.mean(roi, axis=(0, 1)).astype(int)

    # Convert the average color to tuple
    detected_color = tuple(map(int, avg_color))

    # Display the region for color detection
    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

    # Display the detected color and its values in a box on the top right corner
    cv2.rectangle(frame, (0, 0), (200, 50), detected_color, -1)
    cv2.putText(frame, f"Color: {detected_color}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Display the frame
    cv2.imshow('Color Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
