import tkinter as tk
import random

# Not integrated with gui_utils yet

categories = ['SDG 1', 'SDG 2']

questions = {
    'SDG 1': [  ('What is the primary aim of SDG 1 - No Poverty?',
                'To eradicate hunger', 
                'To eliminate poverty in all its forms', 
                'To promote economic growth', 1),
            
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
                 'By promoting biodiversity', 3),]
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
