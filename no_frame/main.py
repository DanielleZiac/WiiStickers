import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from gui_utils import GUIUtils

gui_utils = GUIUtils()

root = gui_utils.root 
root.title("WiiStickers")

width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()

print(width_value, height_value)
x = width_value
y = height_value

canvas = gui_utils.set_background("gui/pages/homePage.png")
button_normal = Image.open("gui/buttons/transparent.png")

other_buttons = [
    {"image_hover": Image.open("gui/buttons/learn.png"), "x": 0.0808, "y": 0.629, "width": 0.88, "height": 0.89, "script_to_run": "learn.py"},
    {"image_hover": Image.open("gui/buttons/start.png"), "x": 0.5703, "y": 0.646, "width": 0.88, "height": 0.89, "script_to_run": "start.py"}
]

gui_utils.create_buttons(canvas, x, y, gui_utils.top_buttons)
gui_utils.create_buttons(canvas, x, y, other_buttons)

root.mainloop()
