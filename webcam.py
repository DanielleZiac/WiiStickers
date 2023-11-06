import cv2
import os
import datetime

# Initialize the webcam and pass a constant which is 0
cam = cv2.VideoCapture(1)

# Title of the app
cv2.namedWindow('OpenCV Webcam App')

# Specify the directory where you want to save the screenshots
save_directory = '/Users/danielleziac/Documents/opencvSTART/sources/'

# Let's assume the number of images taken is 0
img_counter = 0

# While loop
while True:
    # Initialize the frame and ret
    ret, frame = cam.read()
    # If statement
    if not ret:
        print('Failed to grab frame')
        break
    # The frame will be shown with the title 'test'
    cv2.imshow('test', frame)
    # To get continuous live video feed from the laptop's webcam
    k = cv2.waitKey(1)
    # If the escape key is pressed, the app will stop
    if k % 256 == 27:
        print('Escape hit, closing the app')
        break
    # If the spacebar key is pressed, screenshots will be taken
    elif k % 256 == 32:
        # Get the current date and time
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        # The format for storing the images screenshot
        img_name = f'{save_directory}frame_{current_time}.png'
        # Save the image as a PNG file
        cv2.imwrite(img_name, frame)
        print(f'Screenshot taken as {img_name}')
        # The number of images automatically increases by 1
        img_counter += 1

# Release the camera
cam.release()

# Close the camera window
cv2.destroyAllWindows()
print("Current working directory:", os.getcwd())