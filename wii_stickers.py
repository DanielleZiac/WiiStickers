import webbrowser
import json
import re
import random
import os

import sqlite3
from datetime import datetime

import cv2
import dlib
import numpy as np
from imutils import face_utils
import qrcode
from PIL import Image, ImageTk

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.graphics.texture import Texture

db_name = "user_stickers.db"

default_gender = "boy"
default_wear = "polo"
default_color = (255, 255, 255)

opened = "Opened"
closed = "Closed"

eyes_opened = "eyes_opened"
eyes_closed = "eyes_closed"
default_eyes = eyes_opened

mouth_opened = "mouth_opened"
mouth_closed = "mouth_closed"
default_mouth = mouth_closed

default_background = "background_white"
avatar_size = 1100, 1100

max_user_data = 14

questions = {
    'SDG1': [  ('What is the primary aim of SDG 1 - No Poverty?',
                'To eradicate hunger', 
                'To eliminate poverty in all its forms', 
                'To promote economic growth', 2),
            
                ('Which of the following is a key target under SDG 1?',
                'Ensure inclusive and equitable quality education', 
                'End hunger, achieve food security, and improved nutrition', 
                'Ensure availability and sustainable management of water and sanitation for all', 2),

                ('How does implementing education programs contribute to SDG 1?', 
                 'Reducing poverty rates', 
                 'Ensuring clean water access', 
                 'Enhancing environmental sustainability', 3),],

    'SDG2': [  ('What is the main goal of SDG 2 - Zero Hunger?',
                'To eliminate poverty', 
                'To end hunger, achieve food security, and improved nutrition', 
                'To ensure healthy lives and promote well-being for all', 1),
            
                ('Which of the following is a target under SDG 2?',
                'Promote gender equality and empower women', 
                'Achieve gender equality and empower all women and girls', 
                'End all forms of malnutrition and address the nutritional needs of adolescents', 2),

                ('How can sustainable agriculture practices contribute to achieving Zero Hunger?', 
                 'By depleting natural resources', 
                 'By increasing greenhouse gas emissions', 
                 'By promoting biodiversity', 3),],

    'SDG3': [  ('What is the primary focus of SDG 3 - Good Health and Well-being?',
                'Ensure access to clean water and sanitation', 
                'Promote inclusive and sustainable economic growth', 
                'Ensure healthy lives and promote well-being for all at all ages', 1),
            
                ('Which of the following is a specific target under SDG 3?',
                'Ensure access to affordable and clean energy', 
                'Achieve universal health coverage, including financial risk protection', 
                'Combat climate change and its impacts', 2),

                ('How does access to clean water contribute to achieving SDG 3?', 
                 'By reducing the spread of diseases', 
                 'By increasing pollution', 
                 'By promoting inequality', 3),],

    'SDG4': [  ('What is the main objective of SDG 4 (Quality Education)?',
                'Eradicate poverty', 
                'Ensure access to clean water', 
                'Promote inclusive and equitable education', 1),
            
                ('Which target under SDG 4 focuses on promoting lifelong learning opportunities for all?',
                'Target 4.2', 
                'Target 4.5', 
                'Target 4.7', 1)],

    'SDG5': [  ('What is the primary aim of SDG 5 (Gender Equality)?',
                'Achieve universal healthcare', 
                'Ensure equal rights for all genders', 
                'Preserve marine life', 1),
            
                ('Which target under SDG 5 specifically addresses ending violence and harmful practices against women and girls?',
                'Target 5.1', 
                'Target 5.2', 
                'Target 5.4', 1)],

    'SDG6': [  ('What is the key focus of SDG 6 (Clean Water and Sanitation)?',
                'Affordable and clean energy', 
                'Quality education', 
                'Ensuring availability and sustainable management of water and sanitation', 1),
            
                ('Which target under SDG 6 addresses the implementation of integrated water resources management?',
                'Target 6.1', 
                'Target 6.3', 
                'Target 6.6', 1)],

    'SDG7': [  ('What is the primary objective of SDG 7 (Affordable and Clean Energy)?',
                'Zero Hunger', 
                'Ensure access to quality education', 
                'Ensure access to affordable, reliable, sustainable, and modern energy', 1),
            
                ('Which target under SDG 7 focuses on increasing the share of renewable energy in the global energy mix?',
                'Target 7.1', 
                'Target 7.2', 
                'Target 7.3', 1)],

    'SDG8': [  ('What is the main aim of SDG 8 (Decent Work and Economic Growth)?',
                'Quality education for all', 
                'Achieve gender equality', 
                'Promote sustained, inclusive, and sustainable economic growth', 1),
            
                ('Which target under SDG 8 addresses the need to promote inclusive and sustainable industrialization?',
                'Target 8.1', 
                'Target 8.3', 
                'Target 8.5', 1)],

    'SDG9': [  ('What is the main focus of SDG 9?',
                'Quality Education', 
                'Clean Water and Sanitation', 
                'Industry, Innovation, and Infrastructure', 1),
            
                ('How does SDG 9 contribute to sustainable development?',
                'By promoting responsible consumption and production', 
                'By fostering economic growth through innovation and infrastructure development', 
                'By addressing climate change and environmental conservation', 1)],

    'SDG10': [  ('What is the primary aim of SDG 10?',
                'Gender Equality', 
                'Reduced Inequality', 
                'Zero Hunger', 1),
            
                ('How does SDG 10 address inequality?',
                'By promoting access to quality education for all', 
                'By advocating for the rights of marginalized and vulnerable populations ', 
                'By focusing on clean water and sanitation in disadvantaged communities', 1)],

    'SDG11': [  ('What is the focus of SDG 11?',
                'Good Health and Well-being', 
                'Sustainable Cities and Communities', 
                'Climate Action', 1),
            
                ('How does SDG 11 contribute to sustainable development?',
                'By ensuring access to clean energy for all', 
                'By promoting sustainable urban planning and development', 
                'By addressing biodiversity loss and conservation', 1)],

    'SDG12': [  ('What is the main objective of SDG 12?',
                'Quality Education', 
                'Responsible Consumption and Production', 
                'Zero Hunger', 1),
            
                ('How can individuals contribute to achieving SDG 12?',
                'By promoting sustainable and eco-friendly lifestyles', 
                'By advocating for gender equality in the workplace', 
                'By supporting initiatives for clean water and sanitation', 1)],

    'SDG13': [  ('What is the primary focus of SDG 13?',
                'Gender Equality', 
                'Climate Action', 
                'Decent Work and Economic Growth', 1),
            
                ('How does SDG 13 address climate change?',
                'By promoting access to clean water and sanitation', 
                'By fostering economic growth through innovation', 
                'By taking urgent action to combat climate change and its impacts', 1)],

    'SDG14': [  ('What is the focus of SDG 14?',
                'Zero Hunger', 
                'Life Below Water', 
                'Industry, Innovation, and Infrastructure', 1),
            
                ('Why is protecting life below water important for sustainable development?',
                'It contributes to economic growth and job creation', 
                'It helps address poverty and hunger in coastal communities', 
                'It promotes access to quality education for marine life', 1)],

    'SDG15': [  ('What is the main objective of SDG 15?',
                'Affordable and Clean Energy', 
                'Life on Land', 
                'Clean Water and Sanitation', 1),
            
                ('How does SDG 15 contribute to biodiversity conservation?',
                'By promoting sustainable urban development', 
                'By ensuring access to clean water and sanitation in rural areas', 
                'By taking action to protect, restore, and promote sustainable use of terrestrial ecosystems', 1)],

    'SDG16': [  ('What is the primary focus of SDG 16?',
                'Climate Action', 
                'Peace, Justice, and Strong Institutions', 
                'Quality Education', 1),
            
                ('How does SDG 16 contribute to sustainable development?',
                'By promoting access to affordable and clean energy', 
                'By fostering inclusive and accountable institutions at all levels', 
                'By addressing inequalities in income and wealth', 1)],

    'SDG17': [  ('What is the main objective of SDG 17?',
                'Life Below Water', 
                'Partnerships for the Goals', 
                'Zero Hunger', 1),
            
                ('Why are partnerships crucial for achieving sustainable development?',
                'They help address climate change and promote clean energy solutions', 
                'They enhance collaboration between governments, businesses, and civil society', 
                'They focus on reducing inequalities in education', 1)]
}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def open_link(self, link):
        webbrowser.open(link)

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.ids.row_col.text = self.get_table_text()

    def get_table_text(self):
        db = Database(db_name)
        data = db.get_all_data()

        table_text = "------------------------------------------------------------------------------------------------------------------------------------------------------"
        for row in data:
            table_text += self.trim(f"\n{datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')}     {row[2]}, {row[3]}, {row[4]}, {row[5]} {'sticker' if row[5] <= 1 else 'stickers'}")

        if len(data) < max_user_data:
            for i in range(max_user_data - len(data)):
                table_text += f"\n"
        
        return table_text

    def trim(self, text):
        if len(text) > 150:
            return text[:147] + "..."
        
        return text

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
            widget.font_size = 64
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
        button.font_size = 72
        button.color = 0, 0, 1, 1

        self.update_avatar_other_parts()
        self.update_next_button()

    def genderReset(self, button):
        self.is_gender_selected = False
        self.clear_avatar('s1_gender_image')
        self.clear_avatar('s1_eyes_image')
        self.clear_avatar('s1_mouth_image')

        button.font_bold = False
        button.font_size = 64
        button.color = 0, 0, 1, 0.5
        self.update_next_button()

    def wearSelected(self, button):
        self.is_wear_selected = True

        app = App.get_running_app()
        app.selected_wear = button.text
        self.update_avatar_part('s1_wear_image', app.selected_wear)

        button.font_bold = True
        button.font_size = 72
        button.color = 0, 0, 1, 1

        self.update_avatar_other_parts()
        self.update_next_button()

    def wearReset(self, button):
        self.is_wear_selected = False
        self.clear_avatar('s1_wear_image')

        button.font_bold = False
        button.font_size = 64
        button.color = 0, 0, 1, 0.5

        self.update_next_button()

    def update_next_button(self):
        btn = self.ids.next_button

        if self.is_gender_selected and self.is_wear_selected:
            btn.bold = True
            btn.font_size = 72
        else:
            btn.bold = False
            btn.font_size = 64

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
            btn.font_size = 72
        else:
            btn.bold = False
            btn.font_size = 64

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
        app.selected_background = default_background

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
            widget.font_size = 64
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
        button.font_size = 72
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
        button.font_size = 64
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
            btn.font_size = 72
        else:
            btn.bold = False
            btn.font_size = 64

    def on_text_change(self, instance):
        app = App.get_running_app()
        app.input_name = instance[1]

        self.update_next_button()

    def on_next(self):
        if self.is_department_selected and self.ids.input_name.text != "":
            self.manager.current = 'quiz'

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.seconds = 20

    def on_enter(self):
        self.reset()

        self.interval = Clock.schedule_interval(self.update_timer, 1)
        self.generate_random_questions()
        self.render_question()

    def on_leave(self, *args):
        Clock.unschedule(self.interval)  # Stop the scheduled interval

    def reset(self):
        # Reset state
        self.seconds = 20
        self.question_number = 0

        categories = list(questions.keys())
        random.shuffle(categories)
        self.categories = categories

        sdg_init_data = {f"{sdg}": False for sdg in categories}
        self.sdg_quiz_result = sdg_init_data

        # Reset UI
        self.ids.timer_id.text = f"{self.seconds}s"
        self.ids.timer_id.color = 0, 0, 0, 1
        self.ids.score_label.text = "0"

    def update_timer(self, dt):
        self.seconds -= 1
        self.ids.timer_id.text = f"{self.seconds}s"

        if self.seconds <= 5:
            self.ids.timer_id.color = 1, 0, 0, 1

        if self.seconds <= 0:
            self.on_before_switch()
            return False

    def render_question(self):
        sdg = self.categories[self.question_number]

        qn_lbl = self.ids.question_number_label
        qn_lbl.text = f"{self.question_number + 1} / {len(self.categories)}"

        q_btn = self.ids.question_button
        q_btn.text = self.random_questions[sdg][0]

        c1_btn = self.ids.choice1_button
        c1_btn.text = self.random_questions[sdg][1]

        c2_btn = self.ids.choice2_button
        c2_btn.text = self.random_questions[sdg][2]

        c3_btn = self.ids.choice3_button
        c3_btn.text = self.random_questions[sdg][3]

    def is_correct(self, choice):
        sdg = self.categories[self.question_number]
        correct_index = self.random_questions[sdg][4]

        return choice == self.random_questions[sdg][correct_index]

    def update_score(self, value):
        self.sdg_quiz_result[self.categories[self.question_number]] = value
        correct_answers = 0

        for sdg in self.sdg_quiz_result:
            if self.sdg_quiz_result[sdg]:
                correct_answers += 1

        self.ids.score_label.text = f"{correct_answers}"

    def on_next_question(self, button):
        self.update_score(self.is_correct(button.text))

        self.question_number += 1

        if self.question_number < len(self.categories):
            self.render_question()
        else:
            self.on_before_switch()

    def on_before_switch(self):
        app = App.get_running_app()
        app.sdg_quiz_result = json.dumps(self.sdg_quiz_result, indent=4)

        self.manager.current = 'final'

    def generate_random_questions(self):
        categories = list(questions.keys())
        random.shuffle(categories)

        # Create a dictionary to store one random question per category
        random_questions = {}

        # Iterate through the shuffled categories
        for category in categories:
            # Get a random question from the current category
            random_question = random.choice(questions[category])
            
            # Add the random question to the dictionary
            random_questions[category] = random_question

        self.random_questions = random_questions

class FinalScreen(Screen):
    qr_code_generated = False

    def __init__(self, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)

        # init data
        app = App.get_running_app()
        app.sdg_quiz_result = json.dumps({})

    def on_enter(self):
        self.reset()
        self.render_values()

    def reset(self):
        # Reset state
        self.qr_code_generated = False

        # Reset UI
        self.ids.done_button.bold = False
        self.ids.done_button.font_size = 64
        self.ids.done_button.text = "Claim QR Code"
        self.ids.qr_code_image.source = ""
        self.ids.qr_code_image.size = 0, 0
        self.ids.claim_url.text = ""
        self.ids.claim_url.color = 0, 0, 1, 1
        self.ids.input_sr_code.text = ""

    def count_correct_answers(self):
        app = App.get_running_app()
        sdg_quiz_result = json.loads(getattr(app, 'sdg_quiz_result', {}))

        correct_answers = 0

        for sdg in sdg_quiz_result:
            if sdg_quiz_result[sdg]:
                correct_answers += 1

        return correct_answers
    
    def render_values(self):
        app = App.get_running_app()
        name = getattr(app, 'input_name', 'Danielle')

        self.ids.name_label.text = f"{name}"
        self.ids.sticker_number_label.text = f"{self.count_correct_answers()}"
    
    def get_stickers(self):
        app = App.get_running_app()
        sdg_quiz_result = json.loads(getattr(app, 'sdg_quiz_result', {}))

        stickers = ""

        for sdg in sdg_quiz_result:
            if sdg_quiz_result[sdg]:
                if stickers == "":
                    stickers = sdg
                else:
                    stickers = f"{stickers},{sdg}"

        return stickers
    
    def get_name(self):
        app = App.get_running_app()
        name = getattr(app, 'input_name', 'Danielle')

        if len(name) > 12:
            return name[:9] + "..."
        
        return name
    
    def on_text_change(self, instance):
        app = App.get_running_app()
        text_input = instance[1]

        if text_input != "":
            if self.validate_text(text_input):
                btn = self.ids.done_button
                btn.bold = True
                btn.font_size = 72

                app.input_sr_code = text_input

                lbl = self.ids.claim_url
                lbl.text = ""
            else:
                btn = self.ids.done_button
                btn.bold = False
                btn.font_size = 64

                app.input_sr_code = ""

                lbl = self.ids.claim_url
                lbl.text = 'SR code should be in valid format of xx-xxxxx'
                lbl.color = 1, 0, 0, 1

    def generate_qr_code(self):
        app = App.get_running_app()
        input_sr_code = getattr(app, 'input_sr_code', "")
        name = getattr(app, 'input_name', 'Danielle')
        correct_answers = self.count_correct_answers()

        if input_sr_code != "" and self.qr_code_generated:
            department = getattr(app, 'department', "")
            # save user data to database
            db = Database(db_name)
            db.insert_data(input_sr_code, name, department, correct_answers)

            #save image
            self.save_avatar()

            self.manager.current = 'history'
            return

        if input_sr_code != "":
            self.claim_url = f"https://wiistickers.vercel.app?sr-code={input_sr_code}&name={name}&stickers={self.get_stickers()}"
            code = qrcode.QRCode(version=1.0,box_size=15,border=4)
            code.add_data(self.claim_url)
            code.make(fit=True)
            img=code.make_image(fill='Black', back_color= 'White')
            
            # Create a folder with the student ID as the folder name
            folder_path = f"generated_qr_codes/{input_sr_code}"
            os.makedirs(folder_path, exist_ok=True)

            img.save(f"{folder_path}/{name}_{correct_answers}.png")

            self.qr_code_generated = True

            btn = self.ids.done_button
            btn.text = "Done"

            img = self.ids.qr_code_image
            img.source = f"{folder_path}/{name}_{correct_answers}.png"
            img.size = 800, 800

            lbl = self.ids.claim_url
            lbl.text = f"Claim stickers at [ref={self.claim_url}]https://wiistickers.vercel.app[/ref]"
            lbl.color = 0, 0, 1, 1
        else:
            print('no sr code')

    def combine_images(self):
        app = App.get_running_app()
        selected_gender = getattr(app, 'selected_gender', default_gender)
        selected_wear = getattr(app, 'selected_wear', default_wear)
        selected_background = getattr(app, 'selected_background', default_background)
        captured_eyes = getattr(app, 'captured_eyes', default_eyes)
        captured_mouth = getattr(app, 'captured_mouth', default_mouth)
        captured_color = getattr(app, 'captured_color', default_color)

        # Create a new blank image
        final_image = Image.new("RGBA", (400, 400), (255, 255, 255, 0))

        # Layer the images in the specified order (background, gender, collar, eyes, mouth)
        for category in [selected_background, selected_gender, selected_wear, captured_eyes, captured_mouth]:
            feature_image = Image.open(f"gui/avatar/{category}.png")
            feature_image = feature_image.resize((400, 400), Image.BILINEAR)
            final_image.paste(feature_image, (0, 0), feature_image)

        return final_image

    def save_avatar(self):
        app = App.get_running_app()
        input_sr_code = getattr(app, 'input_sr_code', '')

        if input_sr_code:
            # Create a folder with the student ID as the folder name
            folder_path = f"outputs/{input_sr_code}"
            os.makedirs(folder_path, exist_ok=True)

            # Combine selected features to create the final avatar image
            avatar_image = self.combine_images()
            
            # Count existing avatar images in the folder
            existing_images = [f for f in os.listdir(folder_path) if f.startswith("avatar")]
            avatar_number = len(existing_images) + 1
            
            # Save the final image in the student's folder
            final_image_path = f"{folder_path}/avatar{avatar_number}.png"
            avatar_image.save(final_image_path)

    def validate_text(self, text):
        pattern = re.compile(r'^\d{2}-\d{5}$')
        return bool(pattern.match(text))

    def open_claim_url(self):
        webbrowser.open(self.claim_url)

class CustomRectangle(Widget):
    rgba = ListProperty([1, 1, 1, 1])  # Default color: white

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = Rectangle(pos=(370, 350), size=avatar_size)
        self.update_color()  # Initial color setup

    def on_rgba(self, instance, value):
        self.update_color()  # Call the color update method when rgba changes

    def update_color(self):
        self.canvas.before.clear()  # Clear previous canvas instructions
        with self.canvas:
            Color(rgba=self.rgba)
            self.rect = Rectangle(pos=(370, 350), size=avatar_size)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserStickers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_created TEXT,
                sr_code TEXT,
                name TEXT,
                department TEXT,
                num_stickers INTEGER
            )
        ''')
        self.conn.commit()

    def insert_data(self, sr_code, name, department, num_stickers):
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO UserStickers (date_created, sr_code, name, department, num_stickers)
            VALUES (?, ?, ?, ?, ?)
        ''', (date_created, sr_code, name, department, num_stickers))
        self.conn.commit()

    def get_all_data(self):
        self.cursor.execute(f'''
            SELECT * FROM UserStickers
            ORDER BY date_created DESC
            LIMIT {max_user_data}
        ''')
        return self.cursor.fetchall()

class WiiStickersApp(App):
    def build(self):
        Window.maximize()

        sm = ScreenManager()

        # Create screens
        home_screen = HomeScreen(name='home')
        about_screen = AboutScreen(name='about')
        contact_screen = ContactScreen(name='contact')
        history_screen = HistoryScreen(name='history')
        start1_screen = Start1Screen(name='start1')
        start2_screen = Start2Screen(name='start2')
        start3_screen = Start3Screen(name='start3')
        quiz_screen = QuizScreen(name='quiz')
        final_screen = FinalScreen(name='final')

        sm.add_widget(home_screen)
        sm.add_widget(about_screen)
        sm.add_widget(contact_screen)
        sm.add_widget(history_screen)
        sm.add_widget(start1_screen)
        sm.add_widget(start2_screen)
        sm.add_widget(start3_screen)
        sm.add_widget(quiz_screen)
        sm.add_widget(final_screen)

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(sm)

        return root_layout

if __name__ == '__main__':
    WiiStickersApp().run()
