import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class StickerMaker:
    def __init__(self):
        self.image_path = ""
        self.shape = ""
        self.size = (100, 100)
        self.text = ""
        self.text_color = "black"
        self.decorations = []

    def import_photo(self, photo_path: str) -> None:
        self.image_path = photo_path

    def select_shape(self, shape: str) -> None:
        self.shape = shape

    def set_size(self, width: int, height: int) -> None:
        self.size = (width, height)

    def add_text(self, text: str, color: str) -> None:
        self.text = text
        self.text_color = color

    def add_decoration(self, decoration: str) -> None:
        self.decorations.append(decoration)

    def crop_image(self, crop_area: tuple) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            cropped_image = image.crop(crop_area)
            self.image_path = cropped_image

    def resize_image(self, new_size: tuple) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            resized_image = image.resize(new_size)
            self.image_path = resized_image

    def apply_effect(self, effect: str) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            if effect == "grayscale":
                image = image.convert("L")
            self.image_path = image

    def save_sticker(self, file_path: str) -> None:
        if self.image_path:
            self.image_path.save(file_path)

class UserPreferences:
    def __init__(self):
        self.preferences = {}

    def load_preferences(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            self.preferences = json.load(file)

    def save_preferences(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            json.dump(self.preferences, file)

def main():
    root = tk.Tk()
    root.title("Sticker Maker")

    sticker_maker = StickerMaker()
    user_preferences = UserPreferences()
    user_preferences.load_preferences('user_preferences.json')

    # GUI Elements and Logic would be added here

    root.mainloop()

if __name__ == "__main__":
    main()