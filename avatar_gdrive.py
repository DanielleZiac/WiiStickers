import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class AvatarMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("WiiStickers")

        # Initialize variables to store selected features
        self.selected_features = {
            "Background": "background_white.png",
            "Gender": "boy.png",
            "Collar": "roundneck.png",
            "Eyes": "eyesopened.png",
            "Mouth": "mouthopened.png"
        }

        # Create image displaying area
        self.image_area = tk.Label(root)
        self.image_area.pack(pady=10)

        # Create buttons for each feature category
        self.create_feature_buttons("Gender", ["girl.png", "boy.png"])
        self.create_feature_buttons("Collar", ["polo.png", "roundneck.png"])
        self.create_feature_buttons("Eyes", ["eyesopened.png", "eyesclosed.png"])
        self.create_feature_buttons("Mouth", ["mouthopened.png", "mouthclosed.png"])
        self.create_feature_buttons("Background", ["background_white.png", "background_BSU.png", "background_CICS.png", "background_COE.png", "background_CAFAD.png", "background_CIT.png"])

        # Create Save button
        save_button = tk.Button(root, text="Save", command=self.save_avatar)
        save_button.pack(pady=10)

        # Update displayed image with default features
        self.update_displayed_image()

    def authenticate_google_drive(self):
        # Authenticate with Google Drive using PyDrive
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication.

        self.drive = GoogleDrive(gauth)

    def create_feature_buttons(self, category, options):
        # Create label for the feature category
        tk.Label(self.root, text=category).pack()

        # Create buttons for each feature in the category
        for option in options:
            tk.Button(self.root, text=option, command=lambda o=option, c=category: self.set_feature(c, o)).pack()

    def set_feature(self, category, option):
        # Update selected feature for the given category
        self.selected_features[category] = option

        # Update displayed image
        self.update_displayed_image()

    def update_displayed_image(self):
        # Combine selected features to create the avatar
        avatar_image = self.combine_images()

        # Display the avatar image
        #img = ImageTk.PhotoImage(Image.open(avatar_image))
        img = ImageTk.PhotoImage(avatar_image)
        self.image_area.config(image=img)
        self.image_area.image = img

    def combine_images(self):
        # Combine selected features to create the final avatar image
        # You need to implement the logic to layer the images according to your needs
        # For simplicity, let's assume you have a folder named "gui/avatar" with subfolders for each category

        # Create a new blank image
        final_image = Image.new("RGBA", (400, 400), (255, 255, 255, 0))

        # Layer the images in the specified order (background, gender, collar, eyes, mouth)
        for category in ["Background", "Gender", "Collar", "Eyes", "Mouth"]:
            option = self.selected_features[category]
            feature_image = Image.open(f"gui/avatar/{option}")
            feature_image = feature_image.resize((400, 400), Image.BILINEAR)
            final_image.paste(feature_image, (0, 0), feature_image)

        # Save the final image temporarily (you can customize the path)
        #final_image_path = "outputs/temp_avatar.png"
        #final_image.save(final_image_path)

        return final_image

    def save_avatar(self):
        # Prompt the user for a student ID
        student_id = simpledialog.askstring("Student ID", "Enter Student ID:")

        if student_id:
            # Create a folder with the student ID as the folder name
            folder_path = f"outputs/{student_id}"
            os.makedirs(folder_path, exist_ok=True)

            # Combine selected features to create the final avatar image
            avatar_image = self.combine_images()
            
            # Count existing avatar images in the folder
            existing_images = [f for f in os.listdir(folder_path) if f.startswith("avatar")]
            avatar_number = len(existing_images) + 1
            
            # Save the final image in the student's folder
            final_image_path = f"{folder_path}/avatar{avatar_number}.png"
            avatar_image.save(final_image_path)

            print(f"Avatar saved for student ID {student_id} at {final_image_path}")
        else:
            print("Student ID not provided. Avatar not saved.")

    def upload_to_google_drive(self, local_file_path, drive_file_name, drive_folder_path):
        # Upload a file to Google Drive
        file_drive = self.drive.CreateFile({'title': drive_file_name, 'parents': [{'id': drive_folder_path}]})
        file_drive.Upload()

if __name__ == "__main__":
    root = tk.Tk()
    app = AvatarMaker(root)
    root.mainloop()
