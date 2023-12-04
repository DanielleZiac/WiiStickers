import tkinter as tk
from PIL import Image, ImageTk

def create_button(canvas, image_normal, image_hover, x, y, button_width, button_height):
    button_normal = image_normal.resize((button_width, button_height), Image.BILINEAR)
    button_hover = image_hover.resize((button_width, button_height), Image.BILINEAR)

    button_normal = ImageTk.PhotoImage(button_normal)
    button_hover = ImageTk.PhotoImage(button_hover)

    button = canvas.create_image(x, y, anchor=tk.NW, image=button_normal)

    def on_button_click(event):
        print("Button clicked")

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

root = tk.Tk()
root.title("WiiStickers")

width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (width_value, height_value))

bg_image = Image.open("gui/pages/homePage.png")
bg_image = bg_image.resize((width_value, height_value), Image.BILINEAR)
bg_image = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=width_value, height=height_value)
canvas.pack()

bg_label = canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

button_normal = Image.open("gui/buttons/transparent.png")

buttons_data = [
    {"image_hover": Image.open("gui/buttons/home.png"), "x": 0.37, "y": 0.118, "width": 0.89, "height": 0.89},
    {"image_hover": Image.open("gui/buttons/about.png"), "x": 0.4837, "y": 0.118, "width": 0.89, "height": 0.89},
    {"image_hover": Image.open("gui/buttons/contact.png"), "x": 0.6448, "y": 0.118, "width": 0.89, "height": 0.89},
    {"image_hover": Image.open("gui/buttons/history.png"), "x": 0.824, "y": 0.118, "width": 0.89, "height": 0.89},
    {"image_hover": Image.open("gui/buttons/learn.png"), "x": 0.0808, "y": 0.629, "width": 0.88, "height": 0.89},
    {"image_hover": Image.open("gui/buttons/start.png"), "x": 0.5703, "y": 0.646, "width": 0.88, "height": 0.89}
]

for data in buttons_data:
    x = width_value * data["x"]
    y = height_value * data["y"]
    button_width = int(data["image_hover"].width * data["width"])
    button_height = int(data["image_hover"].height * data["height"])

    create_button(
        canvas, button_normal, data["image_hover"],
        x, y, button_width, button_height
    )

root.mainloop()