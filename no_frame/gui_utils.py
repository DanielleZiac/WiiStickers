import tkinter as tk
from PIL import Image, ImageTk
import subprocess


class GUIUtils:
    button_normal = Image.open("gui/buttons/transparent.png")
    top_buttons = [
        {"image_hover": Image.open("gui/buttons/home.png"), "x": 0.3705, "y": 0.1087, "width": 0.95, "height": 0.94, "script_to_run": "main.py"},
        {"image_hover": Image.open("gui/buttons/about.png"), "x": 0.4842, "y": 0.1087, "width": 0.95, "height": 0.94, "script_to_run": "about.py"},
        {"image_hover": Image.open("gui/buttons/contact.png"), "x": 0.6453, "y": 0.1087, "width": 0.95, "height": 0.94, "script_to_run": "contact.py"},
        {"image_hover": Image.open("gui/buttons/history.png"), "x": 0.8245, "y": 0.1087, "width": 0.95, "height": 0.94, "script_to_run": "history.py"},
    ]

    home_buttons = [
        {"image_hover": Image.open("gui/buttons/learn.png"), "x": 0.0808, "y": 0.634, "width": 0.94, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/start.png"), "x": 0.5703, "y": 0.651, "width": 0.94, "height": 0.94, "script_to_run": ""}
    ]

    contact_buttons = [
        {"image_hover": Image.open("gui/buttons/mail.png"), "x": 0.177, "y": 0.417, "width": 0.934, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/github.png"), "x": 0.177, "y": 0.554, "width": 0.934, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/instagram.png"), "x": 0.177, "y": 0.69, "width": 0.934, "height": 0.94, "script_to_run": ""},
    ]

    history_buttons = [
        {"image_hover": Image.open("gui/buttons/details.png"), "x": 0.083, "y": 0.377, "width": 0.93, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/details.png"), "x": 0.083, "y": 0.447, "width": 0.93, "height": 0.94, "script_to_run": ""}
    ]

    start1_buttons = [
        {"image_hover": Image.open("gui/buttons/girl.png"), "x": 0.52, "y": 0.337, "width": 0.93, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/boy.png"), "x": 0.732, "y": 0.337, "width": 0.93, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/polo.png"), "x": 0.52, "y": 0.597, "width": 0.93, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/shirt.png"), "x": 0.732, "y": 0.597, "width": 0.93, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/next.png"), "x": 0.619, "y": 0.751, "width": 0.93, "height": 0.94, "script_to_run": ""},
    ]

    start2_buttons = [
        {"image_hover": Image.open("gui/buttons/capture.png"), "x": 0.496, "y": 0.752, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/next.png"), "x": 0.724, "y": 0.751, "width": 0.933, "height": 0.94, "script_to_run": ""},
    ]

    start2_1_buttons = [
        {"image_hover": Image.open("gui/buttons/recapture.png"), "x": 0.496, "y": 0.752, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/next.png"), "x": 0.724, "y": 0.751, "width": 0.933, "height": 0.94, "script_to_run": ""},
    ]

    start3_buttons = [
        {"image_hover": Image.open("gui/buttons/cics.png"), "x": 0.52, "y": 0.544, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/coe.png"), "x": 0.52, "y": 0.645, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/cit.png"), "x": 0.731, "y": 0.544, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/cafad.png"), "x": 0.731, "y": 0.645, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/next.png"), "x": 0.613, "y": 0.784, "width": 0.933, "height": 0.94, "script_to_run": ""},
    ]

    quiz_buttons = [
        {"image_hover": Image.open("gui/buttons/answer.png"), "x": 0.172, "y": 0.512, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/answer.png"), "x": 0.172, "y": 0.641, "width": 0.933, "height": 0.94, "script_to_run": ""},
        {"image_hover": Image.open("gui/buttons/answer.png"), "x": 0.172, "y": 0.77, "width": 0.933, "height": 0.94, "script_to_run": ""},
    ]

    final_buttons = [
        {"image_hover": Image.open("gui/buttons/done.png"), "x": 0.674, "y": 0.735, "width": 0.94, "height": 0.94, "script_to_run": "main.py"},
    ]
    
    def __init__(self):
        self.root = tk.Tk()
        self.width_value = self.root.winfo_screenwidth()
        self.height_value = self.root.winfo_screenheight()
        self.bg_image = None

    def set_background(self, bg_filename):
        self.root.geometry("%dx%d+0+0" % (self.width_value, self.height_value))
        
        bg_image = Image.open(bg_filename)
        bg_image = bg_image.resize((self.width_value, self.height_value), Image.BILINEAR)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        
        #canvas = tk.Canvas(self.root, width=self.width_value, height=self.height_value)
        #canvas.pack()
        
        bg_label = canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        
        return canvas

    def create_button(self, canvas, image_normal, image_hover, x, y, button_width, button_height, script_to_run):
        button_normal = image_normal.resize((button_width, button_height), Image.BILINEAR)
        button_hover = image_hover.resize((button_width, button_height), Image.BILINEAR)

        button_normal = ImageTk.PhotoImage(button_normal)
        button_hover = ImageTk.PhotoImage(button_hover)

        button = canvas.create_image(x, y, anchor=tk.NW, image=button_normal)

        def on_button_click(event):
            print(script_to_run, "Button clicked")
            self.root.destroy()
            subprocess.run(["python", script_to_run])

        def on_button_hover(event):
            canvas.itemconfig(button, image=button_hover)
            canvas.config(cursor="hand2")

        def on_button_leave(event):
            canvas.itemconfig(button, image=button_normal)
            canvas.config(cursor="")

        canvas.tag_bind(button, "<Button-1>", on_button_click)
        canvas.tag_bind(button, "<Enter>", on_button_hover)
        canvas.tag_bind(button, "<Leave>", on_button_leave)

        return button

    def create_buttons(self, canvas, x, y, button_data_list):
        for data in button_data_list:
            x = self.width_value * data["x"]
            y = self.height_value * data["y"]
            button_width = int(data["image_hover"].width * data["width"])
            button_height = int(data["image_hover"].height * data["height"])

            self.create_button(
                canvas, self.button_normal, data["image_hover"],
                x, y, button_width, button_height,
                data["script_to_run"]
            )

if __name__ == "__main__":
    gui_utils = GUIUtils()
