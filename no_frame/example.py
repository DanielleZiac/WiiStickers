import tkinter as tk

class WindowSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Switcher")

        self.frames = {}

        self.create_frames()
        self.show_frame("MainPage")

    def create_frames(self):
        # Create frames for different "windows" or pages
        main_page = tk.Frame(self.root)
        about_page = tk.Frame(self.root)
        contact_page = tk.Frame(self.root)

        # Add widgets to the frames
        self.add_widgets_to_main_page(main_page)
        self.add_widgets_to_about_page(about_page)
        self.add_widgets_to_contact_page(contact_page)

        # Store frames in a dictionary
        self.frames["MainPage"] = main_page
        self.frames["AboutPage"] = about_page
        self.frames["ContactPage"] = contact_page

    def add_widgets_to_main_page(self, frame):
        label = tk.Label(frame, text="Main Page")
        label.pack()
        button = tk.Button(frame, text="Go to About Page", command=lambda: self.show_frame("AboutPage"))
        button.pack()

    def add_widgets_to_about_page(self, frame):
        label = tk.Label(frame, text="About Page")
        label.pack()
        button = tk.Button(frame, text="Go to Main Page", command=lambda: self.show_frame("MainPage"))
        button.pack()
        button = tk.Button(frame, text="Go to Contact Page", command=lambda: self.show_frame("ContactPage"))
        button.pack()

    def add_widgets_to_contact_page(self, frame):
        label = tk.Label(frame, text="Contact Page")
        label.pack()
        button = tk.Button(frame, text="Go to About Page", command=lambda: self.show_frame("AboutPage"))
        button.pack()

    def show_frame(self, page_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        self.frames[page_name].pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowSwitcherApp(root)
    root.mainloop()
