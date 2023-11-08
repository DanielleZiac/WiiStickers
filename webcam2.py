import cv2
from time import sleep
import os

webcam = cv2.VideoCapture(0)
sleep(2)

while True:
    try:
        check, frame = webcam.read()
        print(check)  # Prints true as long as the webcam is running
        print(frame)  # Prints matrix values of each frame
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(os.path.join('/Users/danielleziac/Documents/opencvSTART/sources/', 'saved_img.jpg'), frame)
            print("Image saved!")

            # Now try to read the saved image for further processing
            try:
                img_ = cv2.imread(os.path.join('/Users/danielleziac/Documents/opencvSTART/sources/', 'saved_img.jpg'), cv2.IMREAD_ANYCOLOR)
                print("Processing image...")
                if img_ is not None:
                    print("Converting RGB image to grayscale...")
                    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                    print("Converted RGB image to grayscale...")
                    print("Resizing image to 30x30 scale...")
                    img_resized = cv2.resize(gray, (640, 640))
                    print("Resized...")
                    cv2.imwrite(os.path.join('/Users/danielleziac/Documents/opencvSTART/sources/', 'saved_img-final.jpg'), img_resized)
                    print("Image saved!")
                else:
                    print("Failed to load the saved image.")
            except Exception as e:
                print(f"Error while processing the saved image: {str(e)}")

        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    except KeyboardInterrupt:
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

print("Current working directory:", os.getcwd())
