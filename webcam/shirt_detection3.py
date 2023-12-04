from glob import glob
import math
import logging

import numpy as np
import cv2


class Shatsu(object):
    def __init__(self, video_capture):
        self.video_capture = video_capture
        self.face_cascade = cv2.CascadeClassifier('./env/lib/python3.12/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
        self.capture_button_pressed = False  # Flag to indicate if the capture button is pressed

    def compress(self, img):
        Z = img.reshape((-1, 3))

        Z = np.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 5

        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10,
                                        cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        return res2

    def detect(self):
        ret, frame = self.video_capture.read()

        blur = cv2.GaussianBlur(frame, (7, 7), 0)
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            logging.debug(f"Error on gray scale conversion")

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        detected = False
        sensitivity = False

        for (x, y, w, h) in faces:
            detected = True

            # bounding rectangle for face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Shirt coordinates
            offset_y_bottom = 70
            offset_x_left = 30
            offset_x_right = 30
            shirt_y = y + h + offset_y_bottom
            shirt_w = w // 3
            shirt_h = w // 3

            try:
                # shirt region 1 (left)
                shirt_x = x + (w // 3) - offset_x_left
                sensitivity_1 = self.shirt_region(blur, shirt_x, shirt_y, shirt_h, shirt_w)
                cv2.rectangle(frame, (shirt_x, shirt_y),
                              (shirt_x+shirt_w, shirt_y+shirt_h), (255, 0, 0), 2)

                # shirt region 2 (right)
                shirt_x = x + (w // 3) + offset_x_right
                sensitivity_2 = self.shirt_region(blur, shirt_x, shirt_y, shirt_h, shirt_w)
                cv2.rectangle(frame, (shirt_x, shirt_y),
                              (shirt_x+shirt_w, shirt_y+shirt_h), (255, 0, 0), 2)

                # shirt region 3 (bottom)
                shirt_y = y + h + 130
                shirt_x = x + (w // 3)
                sensitivity_3 = self.shirt_region(blur, shirt_x, shirt_y, shirt_h, shirt_w)
                cv2.rectangle(frame, (shirt_x, shirt_y),
                              (shirt_x+shirt_w, shirt_y+shirt_h), (255, 0, 0), 2)

                sensitivity = sensitivity_1 or sensitivity_2 or sensitivity_3
                break
            except cv2.error:
                logging.debug(f"Error in K means")
                continue
            except ZeroDivisionError:
                logging.debug(f"Division by Zero")
                continue

        if detected:
            # Display real-time color of the shirt
            cv2.putText(frame, f"Shirt Color: RGB({sensitivity[0]}, {sensitivity[1]}, {sensitivity[2]})", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Display the frame
            cv2.imshow('Shirt Detection', frame)

            # Check if the capture button is pressed
            if self.capture_button_pressed:
                # Save the color-detected image
                self.save_image(frame, sensitivity)
                self.capture_button_pressed = False  # Reset the flag

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            self.video_capture.release()
            cv2.destroyAllWindows()
        elif k == ord('c'):  # Check for the 'c' key press for capturing the color
            self.capture_button_pressed = True

    def save_image(self, frame, sensitivity):
        # Create an image with the detected color
        color_image = np.zeros((100, 100, 3), dtype=np.uint8)
        color_image[:, :] = sensitivity

        # Concatenate the original frame and the color image
        result_image = np.hstack((frame, color_image))

        # Save the result image
        cv2.imwrite('captured_shirt_color.jpg', result_image)
        logging.info("Color-detected image captured.")
        
    def shirt_region(self, blur, shirt_x, shirt_y, shirt_h, shirt_w):
        crop_img = blur[shirt_y:shirt_y+shirt_h, shirt_x:shirt_x+shirt_w]
        crop_img = self.compress(crop_img)

        avg_color_per_row = np.average(crop_img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

        r, g, b = map(lambda x: int(x) if not math.isnan(x) else x,
                      [avg_color[2], avg_color[1], avg_color[0]])

        return [r, g, b]

    def color_detect(self, img):
        confidence = 0
        for row in img:
            for b, g, r in row:
                diff = abs(g-b)
                if diff <= 20 and max(g, b) - 20 >= r:
                    confidence += 1
        return str(int((confidence / (img.shape[0]*img.shape[1])) * 100))

    def check_uniform(self, *rgb):
        r, g, b = rgb
        diff = abs(g-b)

        return True if diff <= 20 and max(g, b) - 20 >= r else False


if __name__ == '__main__':
    logging.basicConfig(filename='/var/tmp/shirt.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)

    video_capture = cv2.VideoCapture(0)

    shatsu_obj = Shatsu(video_capture)

    while True:
        shatsu_obj.detect()
