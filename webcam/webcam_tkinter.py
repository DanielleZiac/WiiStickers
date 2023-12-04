import cv2
import os
import datetime
import tkinter as tk

class WebcamApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam App")

        # Initialize the webcam and pass a constant which is 0
        self.cam = cv2.VideoCapture(0)

        # Specify the directory where you want to save the screenshots
        self.save_directory = '/Users/danielleziac/Documents/WiiStickers/sources/'

        # Set the camera resolution to the maximum available
        self.cam.set(3, 1920)  # Width
        self.cam.set(4, 1080)  # Height
        
        self.img_counter = 0

        self.setup_gui()
        self.update_webcam()

        # Set the frame rate (e.g., 30 frames per second)
        self.cam.set(cv2.CAP_PROP_FPS, 60)

    def setup_gui(self):
        self.canvas = tk.Canvas(self.window, width=1920, height=1080)
        self.canvas.grid(row=0, column=0, columnspan=2)  # Adjust the columnspan to 2 to make it span two columns

        self.btn_capture = tk.Button(self.window, text="Capture", command=self.capture_image)
        self.btn_capture.grid(row=1, column=0, columnspan=2)  # Place the button in the next row

    def update_webcam(self):
        ret, frame = self.cam.read()

        if ret:
            self.current_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = self.image_to_tkinter_format(self.current_image)

            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.window.after(15, self.update_webcam)

    def image_to_tkinter_format(self, image):
        return tk.PhotoImage(data=self.pil_to_tkinter_format(image))

    def pil_to_tkinter_format(self, image):
        from PIL import Image
        import io
        image_pil = Image.fromarray(image)
        img_bytes = io.BytesIO()
        image_pil.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.read()

    def capture_image(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        img_name = os.path.join(self.save_directory, f'frame_{current_time}.png')
        cv2.imwrite(img_name, self.current_image)
        print(f'Screenshot taken as {img_name}')
        self.img_counter += 1

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    app.run()
