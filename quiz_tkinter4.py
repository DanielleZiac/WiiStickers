import tkinter as tk
import random

# Not integrated with gui_utils yet

categories = ['SDG 1', 'SDG 2', 'SDG 3', 'SDG 4', 'SDG 5', 'SDG 6', 'SDG 7', 'SDG 8', 'SDG 9', 'SDG 10', 'SDG 11', 'SDG 12', 'SDG 13', 'SDG 14', 'SDG 15', 'SDG 16', 'SDG 17']

questions = {
    'SDG 1': [  ('What is the primary aim of SDG 1 - No Poverty?',
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

    'SDG 2': [  ('What is the main goal of SDG 2 - Zero Hunger?',
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

    'SDG 3': [  ('What is the primary focus of SDG 3 - Good Health and Well-being?',
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

    'SDG 4': [  ('What is the main objective of SDG 4 (Quality Education)?',
                'Eradicate poverty', 
                'Ensure access to clean water', 
                'Promote inclusive and equitable education', 1),
            
                ('Which target under SDG 4 focuses on promoting lifelong learning opportunities for all?',
                'Target 4.2', 
                'Target 4.5', 
                'Target 4.7', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 5': [  ('What is the primary aim of SDG 5 (Gender Equality)?',
                'Achieve universal healthcare', 
                'Ensure equal rights for all genders', 
                'Preserve marine life', 1),
            
                ('Which target under SDG 5 specifically addresses ending violence and harmful practices against women and girls?',
                'Target 5.1', 
                'Target 5.2', 
                'Target 5.4', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 6': [  ('What is the key focus of SDG 6 (Clean Water and Sanitation)?',
                'Affordable and clean energy', 
                'Quality education', 
                'Ensuring availability and sustainable management of water and sanitation', 1),
            
                ('Which target under SDG 6 addresses the implementation of integrated water resources management?',
                'Target 6.1', 
                'Target 6.3', 
                'Target 6.6', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 7': [  ('What is the primary objective of SDG 7 (Affordable and Clean Energy)?',
                'Zero Hunger', 
                'Ensure access to quality education', 
                'Ensure access to affordable, reliable, sustainable, and modern energy', 1),
            
                ('Which target under SDG 7 focuses on increasing the share of renewable energy in the global energy mix?',
                'Target 7.1', 
                'Target 7.2', 
                'Target 7.3', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 8': [  ('What is the main aim of SDG 8 (Decent Work and Economic Growth)?',
                'Quality education for all', 
                'Achieve gender equality', 
                'Promote sustained, inclusive, and sustainable economic growth', 1),
            
                ('Which target under SDG 8 addresses the need to promote inclusive and sustainable industrialization?',
                'Target 8.1', 
                'Target 8.3', 
                'Target 8.5', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 9': [  ('What is the main focus of SDG 9?',
                'Quality Education', 
                'Clean Water and Sanitation', 
                'Industry, Innovation, and Infrastructure', 1),
            
                ('How does SDG 9 contribute to sustainable development?',
                'By promoting responsible consumption and production', 
                'By fostering economic growth through innovation and infrastructure development', 
                'By addressing climate change and environmental conservation', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 10': [  ('What is the primary aim of SDG 10?',
                'Gender Equality', 
                'Reduced Inequality', 
                'Zero Hunger', 1),
            
                ('How does SDG 10 address inequality?',
                'By promoting access to quality education for all', 
                'By advocating for the rights of marginalized and vulnerable populations ', 
                'By focusing on clean water and sanitation in disadvantaged communities', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 11': [  ('What is the focus of SDG 11?',
                'Good Health and Well-being', 
                'Sustainable Cities and Communities', 
                'Climate Action', 1),
            
                ('How does SDG 11 contribute to sustainable development?',
                'By ensuring access to clean energy for all', 
                'By promoting sustainable urban planning and development', 
                'By addressing biodiversity loss and conservation', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 12': [  ('What is the main objective of SDG 12?',
                'Quality Education', 
                'Responsible Consumption and Production', 
                'Zero Hunger', 1),
            
                ('How can individuals contribute to achieving SDG 12?',
                'By promoting sustainable and eco-friendly lifestyles', 
                'By advocating for gender equality in the workplace', 
                'By supporting initiatives for clean water and sanitation', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 13': [  ('What is the primary focus of SDG 13?',
                'Gender Equality', 
                'Climate Action', 
                'Decent Work and Economic Growth', 1),
            
                ('How does SDG 13 address climate change?',
                'By promoting access to clean water and sanitation', 
                'By fostering economic growth through innovation', 
                'By taking urgent action to combat climate change and its impacts', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 14': [  ('What is the focus of SDG 14?',
                'Zero Hunger', 
                'Life Below Water', 
                'Industry, Innovation, and Infrastructure', 1),
            
                ('Why is protecting life below water important for sustainable development?',
                'It contributes to economic growth and job creation', 
                'It helps address poverty and hunger in coastal communities', 
                'It promotes access to quality education for marine life', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 15': [  ('What is the main objective of SDG 15?',
                'Affordable and Clean Energy', 
                'Life on Land', 
                'Clean Water and Sanitation', 1),
            
                ('How does SDG 15 contribute to biodiversity conservation?',
                'By promoting sustainable urban development', 
                'By ensuring access to clean water and sanitation in rural areas', 
                'By taking action to protect, restore, and promote sustainable use of terrestrial ecosystems', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 16': [  ('What is the primary focus of SDG 16?',
                'Climate Action', 
                'Peace, Justice, and Strong Institutions', 
                'Quality Education', 1),
            
                ('How does SDG 16 contribute to sustainable development?',
                'By promoting access to affordable and clean energy', 
                'By fostering inclusive and accountable institutions at all levels', 
                'By addressing inequalities in income and wealth', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),],

    'SDG 17': [  ('What is the main objective of SDG 17?',
                'Life Below Water', 
                'Partnerships for the Goals', 
                'Zero Hunger', 1),
            
                ('Why are partnerships crucial for achieving sustainable development?',
                'They help address climate change and promote clean energy solutions', 
                'They enhance collaboration between governments, businesses, and civil society', 
                'They focus on reducing inequalities in education', 1),

                ('QUESTION',
                'CHOICE', 
                'CHOICE', 
                'CHOICE', 1),]
}


class QuizPage:
    def __init__(self, master, questions):
        self.master = master
        self.questions = questions
        self.category_order = random.sample(list(questions.keys()), len(questions))
        self.questions_order = self.generate_questions_order()
        self.current_question_index = 0
        self.score = 0
        self.correct_categories = set()
        self.create_widgets()

    def generate_questions_order(self):
        # Select one random question from each category
        return [(category, random.choice(self.questions[category])) for category in self.category_order]

    def create_widgets(self):
        self.label = tk.Label(self.master, text="")
        self.label.pack()

        self.choice_buttons = []
        for i in range(1, 4):
            button = tk.Button(self.master, text="", command=lambda choice=i: self.check_answer(choice))
            button.pack()
            self.choice_buttons.append(button)

        self.next_question()

    def next_question(self):
        if self.current_question_index < len(self.questions_order):
            category, question_data = self.questions_order[self.current_question_index]

            question, choice1, choice2, choice3, _ = question_data
            self.label.config(text=f'{category} - {question}')

            # Display choices in their original order
            for i, button in enumerate(self.choice_buttons):
                button.config(text=f'{i + 1}. {question_data[i + 1]}')
        else:
            self.show_result()

    def check_answer(self, user_answer):
        # Check if the user's answer is correct, update score, and move to the next question
        category, question_data = self.questions_order[self.current_question_index]
        _, _, _, _, correct_answer = question_data

        if user_answer == correct_answer:
            self.score += 1
            self.correct_categories.add(category)

        self.current_question_index += 1

        self.next_question()

    def show_result(self):
        # Destroy choice buttons
        for button in self.choice_buttons:
            button.destroy()

        result_text = f'Your final score is: {self.score}/{len(self.questions_order)}\nCategories with the correct answers:\n'

        # Add correct categories to the result text
        if self.correct_categories:
            for category in self.correct_categories:
                result_text += f'{category}\n'
        else:
            result_text += 'None\n'

        # Update the label text
        self.label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quiz Page")

    app = QuizPage(root, questions)

    root.mainloop()
