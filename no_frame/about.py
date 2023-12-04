import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from gui_utils import GUIUtils

gui_utils = GUIUtils()

root = gui_utils.root
root.title("WiiStickers")
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()

x = width_value
y = height_value

canvas = gui_utils.set_background("gui/pages/aboutPage.png")
button_normal = Image.open("gui/buttons/transparent.png")

gui_utils.create_buttons(canvas, x, y, gui_utils.top_buttons)

root.mainloop()
