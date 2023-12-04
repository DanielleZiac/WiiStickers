import tkinter as tk
from PIL import Image, ImageTk

class GUIUtils:
    button_normal = Image.open("gui/buttons/transparent.png")
    top_buttons = [
        {"image_hover": Image.open("gui/buttons/home.png"), "x": 0.3705, "y": 0.1087, "width": 0.95, "height": 0.94, "page_name": "home_page"},
        {"image_hover": Image.open("gui/buttons/about.png"), "x": 0.4842, "y": 0.1087, "width": 0.95, "height": 0.94, "page_name": "about_page"},
        {"image_hover": Image.open("gui/buttons/contact.png"), "x": 0.6453, "y": 0.1087, "width": 0.95, "height": 0.94, "page_name": "contact_page"},
        {"image_hover": Image.open("gui/buttons/history.png"), "x": 0.8245, "y": 0.1087, "width": 0.95, "height": 0.94, "page_name": "history_page"},
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
        
        canvas = tk.Canvas(self.root, width=self.width_value, height=self.height_value)
        canvas.pack()
        
        bg_label = canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        
        return canvas

    def create_button(self, canvas, image_normal, image_hover, x, y, button_width, button_height, callback):
        button_normal = image_normal.resize((button_width, button_height), Image.BILINEAR)
        button_hover = image_hover.resize((button_width, button_height), Image.BILINEAR)

        button_normal = ImageTk.PhotoImage(button_normal)
        button_hover = ImageTk.PhotoImage(button_hover)

        button = canvas.create_image(x, y, anchor=tk.NW, image=button_normal)

        if data["page_name"] == "home_page":
            callback = Buttons.home_page
        elif data["page_name"] == "contact_page":
            callback = Buttons.contact_page
            
        def on_button_click(event):
            print(data[page_name], "Button clicked")
            # callback()
            pass

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
                callback
            )

if __name__ == "__main__":
    gui_utils = GUIUtils()

class Buttons:
    def __init__(self):
        self.root = tk.Tk()
        self.width_value = self.root.winfo_screenwidth()
        self.height_value = self.root.winfo_screenheight()
        self.bg_image = None

    @staticmethod
    def home_page():
        root = gui_utils.root
        root.title("WiiStickers")

        width_value = root.winfo_screenwidth()
        height_value = root.winfo_screenheight()

        x = width_value
        y = height_value

        canvas = gui_utils.set_background("gui/pages/homePage.png")
        button_normal = Image.open("gui/buttons/transparent.png")

        home_buttons = [
            {"image_hover": Image.open("gui/buttons/learn.png"), "x": 0.0808, "y": 0.634, "width": 0.94, "height": 0.94, "page_name": "learn_page"},
            {"image_hover": Image.open("gui/buttons/start.png"), "x": 0.5703, "y": 0.651, "width": 0.94, "height": 0.94, "page_name": "start_page"}
        ]

        gui_utils.create_buttons(canvas, x, y, gui_utils.top_buttons)
        gui_utils.create_buttons(canvas, x, y, home_buttons)

        root.mainloop()

    @staticmethod
    def contact_page():
        # destroy previous page buttons

        contact_buttons = [
            {"image_hover": Image.open("gui/buttons/mail.png"), "x": 0.177, "y": 0.417, "width": 0.934, "height": 0.94, "page_name": "mail_page"},
            {"image_hover": Image.open("gui/buttons/github.png"), "x": 0.177, "y": 0.554, "width": 0.934, "height": 0.94, "page_name": "github_page"},
            {"image_hover": Image.open("gui/buttons/instagram.png"), "x": 0.177, "y": 0.69, "width": 0.934, "height": 0.94, "page_name": "instagram_page"},
        ]        
        
        canvas = gui_utils.set_background("gui/pages/contactPage.png")

        gui_utils.create_buttons(canvas, x, y, gui_utils.top_buttons)
        gui_utils.create_buttons(canvas, x, y, contact_buttons)

if __name__ == "__main__":
    Buttons.home_page()
