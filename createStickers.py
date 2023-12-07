import os
import re
import json
import qrcode
import random
import sqlite3
import webbrowser
from PIL import Image
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import  Screen

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
        self.ids.done_button.font_size = 70
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
                btn.font_size = 80

                app.input_sr_code = text_input

                lbl = self.ids.claim_url
                lbl.text = ""
            else:
                btn = self.ids.done_button
                btn.bold = False
                btn.font_size = 70

                app.input_sr_code = ""

                lbl = self.ids.claim_url
                lbl.text = 'SR code should be in valid format of xx-xxxxx'
                lbl.color = 1, 0, 0, 1

    def generate_qr_code(self):
        app = App.get_running_app()
        input_sr_code = getattr(app, 'input_sr_code', "")
        name = getattr(app, 'input_name', '')
        selected_gender = getattr(app, 'selected_gender', '')
        selected_wear = getattr(app, 'selected_wear', '')
        selected_background = getattr(app, 'selected_background', '')
        captured_mouth = getattr(app, 'captured_mouth', "")
        captured_eyes = getattr(app, 'captured_eyes', "")
        captured_color = getattr(app, 'captured_color', "")
        b, g, r = captured_color

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
            claim_url = f"https://wiistickers.vercel.app/?name={name}&dept={selected_background}&sr-code={input_sr_code}&stickers={self.get_stickers()}&gender={selected_gender}&mouth={captured_mouth}&eyes={captured_eyes}&wear={selected_wear}&bg=({r},{g},{b},1)"
            self.claim_url = claim_url
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
        self.rect = Rectangle(pos=(440, 300), size=avatar_size)
        self.update_color()  # Initial color setup

    def on_rgba(self, instance, value):
        self.update_color()  # Call the color update method when rgba changes

    def update_color(self):
        self.canvas.before.clear()  # Clear previous canvas instructions
        with self.canvas:
            Color(rgba=self.rgba)
            self.rect = Rectangle(pos=(440, 300), size=avatar_size)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserStickers (
                avatar_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
