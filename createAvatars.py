import cv2
import json
import dlib
import numpy as np
from imutils import face_utils

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen

db_name = "user_stickers.db"

default_gender = "boy"
default_wear = "polo"
default_color = (255, 255, 255)

opened = "Opened"
closed = "Closed"

eyes_opened = "eyes_opened"
eyes_closed = "eyes_closed"

mouth_opened = "mouth_opened"
mouth_closed = "mouth_closed"

default_eyes = eyes_opened
default_mouth = mouth_closed

default_background = "background_white"
avatar_size = 1120, 1120

class Start1Screen(Screen):
    def __init__(self, **kwargs):
        super(Start1Screen, self).__init__(**kwargs)
        self.is_gender_selected = False
        self.is_wear_selected = False

    def on_enter(self):
        self.reset()
        self.reset_app_state()

    def reset(self):
        # Reset state
        self.is_gender_selected = False
        self.is_wear_selected = False

        # Reset UI
        self.ids.s1_shirt_color.rgba = 1, 1, 1, 1
        self.update_next_button()

        widget_ids = ['s1_gender_image', 's1_wear_image', 's1_eyes_image', 's1_mouth_image']

        for widget_id in widget_ids:
            setattr(self.ids[widget_id], 'source', '')

        widgets = [
            self.ids.girl_gender_id,
            self.ids.boy_gender_id,
            self.ids.polo_wear_id,
            self.ids.shirt_wear_id
        ]

        for widget in widgets:
            widget.state = "normal"
            widget.font_size = 70
            widget.font_bold = False
            widget.color = (0, 0, 1, 0.5)

    def reset_app_state(self):
        app = App.get_running_app()
        app.selected_gender = default_gender
        app.selected_wear = default_wear
        app.selected_background = default_background
        app.captured_eyes = default_eyes
        app.captured_mouth = mouth_closed
        app.captured_color = default_color
        app.input_name = ""
        app.sdg_quiz_result = json.dumps({})
        app.input_sr_code = ""
        app.department = ""

    def update_avatar_part(self, image_id, value):
        img = self.ids[image_id]
        img.source = "gui/avatar/" + value + ".png"
        img.size = avatar_size

    def update_avatar_other_parts(self):
        self.update_avatar_part('s1_background_image', default_background)

        # Set shirt color to a default color converted from RGB to RGBA
        self.ids.s1_shirt_color.rgba = tuple(x / 255 for x in default_color) + (1,)

    def clear_avatar(self, image_id):
        img = self.ids[image_id]
        img.source = ""
        img.size = 0, 0

    def genderSelected(self, button):
        self.is_gender_selected = True

        app = App.get_running_app()
        app.selected_gender = button.text
        self.update_avatar_part('s1_gender_image', app.selected_gender)
        self.update_avatar_part('s1_eyes_image', default_eyes)
        self.update_avatar_part('s1_mouth_image', default_mouth)

        button.font_bold = True
        button.font_size = 80
        button.color = 0, 0, 1, 1

        self.update_avatar_other_parts()
        self.update_next_button()

    def genderReset(self, button):
        self.is_gender_selected = False
        self.clear_avatar('s1_gender_image')
        self.clear_avatar('s1_eyes_image')
        self.clear_avatar('s1_mouth_image')

        button.font_bold = False
        button.font_size = 70
        button.color = 0, 0, 1, 0.5
        self.update_next_button()

    def wearSelected(self, button):
        self.is_wear_selected = True

        app = App.get_running_app()
        app.selected_wear = button.text
        self.update_avatar_part('s1_wear_image', app.selected_wear)

        button.font_bold = True
        button.font_size = 80
        button.color = 0, 0, 1, 1

        self.update_avatar_other_parts()
        self.update_next_button()

    def wearReset(self, button):
        self.is_wear_selected = False
        self.clear_avatar('s1_wear_image')

        button.font_bold = False
        button.font_size = 70
        button.color = 0, 0, 1, 0.5

        self.update_next_button()

    def update_next_button(self):
        btn = self.ids.next_button

        if self.is_gender_selected and self.is_wear_selected:
            btn.bold = True
            btn.font_size = 80
        else:
            btn.bold = False
            btn.font_size = 70

    def on_next(self):
        if self.is_gender_selected and self.is_wear_selected:
            self.manager.current = 'start2'

class Start2Screen(Screen):
    def __init__(self, **kwargs):
        super(Start2Screen, self).__init__(**kwargs)

    def on_pre_enter(self):
        self.reset()

    def on_enter(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.video_capture = cv2.VideoCapture(0)

        # Set the region for color detection (bottom center)
        self.rect_x, self.rect_y = 600, 600
        self.rect_width, self.rect_height = 200, 100

        # Initialize image to render camera feed
        camera_feed = self.ids.camera_feed
        camera_feed.size = 1400, 900
        self.image = camera_feed

        # Schedule the update function to run every frame
        self.interval = Clock.schedule_interval(self.on_update, 1.0 / 30.0)  # Update every 30 frames per second

    def reset(self):
        # Reset state
        self.counter = 0 # to remove
        self.captured = False
        self.captured_eyes = default_eyes
        self.captured_mouth = mouth_closed
        self.captured_color = default_color

        app = App.get_running_app()
        app.captured_eyes = self.captured_eyes
        app.captured_mouth = self.captured_mouth
        app.captured_color = self.captured_color

        # Reset UI
        self.ids.s2_shirt_color.rgba = 1, 1, 1, 1
        self.ids.capture_button.text = "Capture"
        self.ids.camera_feed.size = 0, 0
        self.ids.camera_feed.source = ""
        self.update_avatar()
        self.update_next_button()
    
    def on_leave(self, *args):
        Clock.unschedule(self.interval)  # Stop the scheduled interval

        if hasattr(self, 'video_capture') and self.video_capture.isOpened():
            self.video_capture.release()  # Release video capture when leaving the screen

    def update_avatar_parts(self, image_id, value):
        img = self.ids[image_id]
        img.source = "gui/avatar/" + value + ".png"
        img.size = avatar_size

    def update_avatar(self):
        captured_eyes = self.captured_eyes
        captured_mouth = self.captured_mouth
        captured_color = self.captured_color

        app = App.get_running_app()
        selected_gender = getattr(app, 'selected_gender', default_gender)
        selected_wear = getattr(app, 'selected_wear', default_wear)
        selected_background = getattr(app, 'selected_background', default_background)

        if self.captured:
            captured_eyes = getattr(app, 'captured_eyes', default_eyes)
            captured_mouth = getattr(app, 'captured_mouth', default_mouth)
            captured_color = getattr(app, 'captured_color', default_color)

        self.update_avatar_parts('s2_background_image', selected_background)
        self.update_avatar_parts('s2_gender_image', selected_gender)
        self.update_avatar_parts('s2_wear_image', selected_wear)
        self.update_avatar_parts('s2_eyes_image', captured_eyes)
        self.update_avatar_parts('s2_mouth_image', captured_mouth)

        # Set shirt color to a captured color converted from RGB to RGBA
        b, g, r = [val / 255.0 for val in captured_color]
        self.ids.s2_shirt_color.rgba = (r, g, b, 1)

    def on_update(self, dt):
        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()

            if ret:
                if not self.captured:
                    self.display_status(frame)
                    self.detect_face(frame)
                    self.detect_color(frame)
                else:
                    # Display the captured statuses
                    self.display_status(frame)

                # Display the resulting frame
                buf = cv2.flip(frame, 0).tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = image_texture
        
        self.update_avatar()
        self.update_next_button()

    def update_next_button(self):
        btn = self.ids.next_button

        if self.captured:
            btn.bold = True
            btn.font_size = 80
        else:
            btn.bold = False
            btn.font_size = 70

    def detect_color(self, frame):
        # Display the region for color detection
        pt1 = (self.rect_x, self.rect_y)
        pt2 = (self.rect_x + self.rect_width, self.rect_y + self.rect_height)
        cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

        # Get the average color of the region
        roi = frame[self.rect_y:self.rect_y + self.rect_height - 10, self.rect_x:self.rect_x + self.rect_width - 10]
        avg_color = np.mean(roi, axis=(0, 1)).astype(int)
        detected_color = tuple(map(int, avg_color))

        # Update the statuses
        self.captured_color = detected_color

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if not faces:
            cv2.putText(frame, "No face detected", (10, 360),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            return
        
        for face in faces:
            shape = self.predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            # Extract coordinates for eyes
            left_eye = shape[42:48]
            right_eye = shape[36:42]

            # Draw the eyes on the frame
            for (x, y) in left_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            for (x, y) in right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Determine if eyes are open or closed
            left_eye_distance = shape[47][1] - shape[43][1]
            right_eye_distance = shape[41][1] - shape[37][1]
            self.captured_eyes = eyes_closed if left_eye_distance < 15 and right_eye_distance < 15 else eyes_opened

            # Extract coordinates for mouth
            mouth = shape[48:68]

            # Draw the mouth on the frame
            for (x, y) in mouth:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Determine if mouth is open or closed
            self.captured_mouth = mouth_opened if shape[66][1] - shape[62][1] > 10 else mouth_closed

    def display_status(self, frame):
        # Display the captured statuses on the frame
        cv2.putText(frame, f"Eyes: {opened if self.captured_eyes == eyes_opened else closed}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.putText(frame, f"Mouth: {opened if self.captured_mouth == mouth_opened else closed}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.putText(frame, f"Color: {self.captured_color}", (10, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.rectangle(frame, (15, 300), (200, 200), self.captured_color , -1)
        
    def on_capture(self):
        app = App.get_running_app()

        btn = self.ids.capture_button

        if self.captured:
            self.captured = False
            btn.text = "Capture"
        else:
            self.captured = True
            btn.text = "Reset"

            app.captured_eyes = self.captured_eyes
            app.captured_mouth = self.captured_mouth
            app.captured_color = self.captured_color

    def on_next(self):
        if self.captured:
            self.manager.current = 'start3'


class Start3Screen(Screen):
    def __init__(self, **kwargs):
        super(Start3Screen, self).__init__(**kwargs)

    def on_enter(self):
        self.reset()
        self.set_avatar()

    def reset(self):
        # Reset state
        self.is_department_selected = False

        app = App.get_running_app()
        #app.selected_background = default_background
        app.selected_background = "background_BSU"

        # Reset UI
        self.ids.s3_shirt_color.rgba = 1, 1, 1, 1
        self.update_next_button()
        self.ids.input_name.text = ""

        widgets = [
            self.ids.cafad_dept_id,
            self.ids.cics_dept_id,
            self.ids.cit_dept_id,
            self.ids.coe_dept_id
        ]

        for widget in widgets:
            widget.state = "normal"
            widget.font_size = 70
            widget.font_bold = False
            widget.color = (0, 0, 1, 0.5)

    def set_avatar_parts(self, image_id, value):
        img = self.ids[image_id]
        img.source = "gui/avatar/" + value + ".png"
        img.size = avatar_size

    def set_avatar(self):
        app = App.get_running_app()
        selected_gender = getattr(app, 'selected_gender', default_gender)
        selected_wear = getattr(app, 'selected_wear', default_wear)
        selected_background = getattr(app, 'selected_background', default_background)
        captured_eyes = getattr(app, 'captured_eyes', default_eyes)
        captured_mouth = getattr(app, 'captured_mouth', default_mouth)
        captured_color = getattr(app, 'captured_color', default_color)

        self.set_avatar_parts('s3_background_image', selected_background)
        self.set_avatar_parts('s3_gender_image', selected_gender)
        self.set_avatar_parts('s3_wear_image', selected_wear)
        self.set_avatar_parts('s3_eyes_image', captured_eyes)
        self.set_avatar_parts('s3_mouth_image', captured_mouth)

        # Set shirt color to a captured color converted from RGB to RGBA
        b, g, r = [val / 255.0 for val in captured_color]
        self.ids.s3_shirt_color.rgba = (r, g, b, 1)

    def update_background(self):
        app = App.get_running_app()
        self.set_avatar_parts('s3_background_image', app.selected_background)

    def departmentSelected(self, button):
        self.is_department_selected = True

        button.font_bold = True
        button.font_size = 80
        button.color = 0, 0, 1, 1

        # Set the selected department
        app = App.get_running_app()
        app.department = button.text
        app.selected_background = "background_" + button.text
        self.set_avatar_parts('s3_background_image', app.selected_background)

        self.update_background()
        self.update_next_button()

    def departmentReset(self, button):
        self.is_department_selected = False

        button.font_bold = False
        button.font_size = 70
        button.color = 0, 0, 1, 0.5

        # Set background to default
        app = App.get_running_app()
        app.selected_background = default_background

        self.update_background()
        self.update_next_button()

    def update_next_button(self):
        btn = self.ids.next_button

        if self.is_department_selected and self.ids.input_name.text != "":
            btn.bold = True
            btn.font_size = 80
        else:
            btn.bold = False
            btn.font_size = 70

    def on_text_change(self, instance):
        app = App.get_running_app()
        app.input_name = instance[1]

        self.update_next_button()

    def on_next(self):
        if self.is_department_selected and self.ids.input_name.text != "":
            self.manager.current = 'quiz'
