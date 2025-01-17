import os
import json
from PIL import Image, ImageDraw, ImageFont

class PhotoEditor:
    def __init__(self):
        self.image_path = ""
        self.shape = ""
        self.size = (100, 100)
        self.text = ""
        self.user_preferences_file = 'user_preferences.json'
        self.load_user_preferences()

    def import_photo(self, file_path: str) -> None:
        if os.path.exists(file_path):
            self.image_path = file_path
        else:
            raise FileNotFoundError("The specified file does not exist.")

    def choose_shape(self, shape: str) -> None:
        self.shape = shape

    def set_size(self, width: int, height: int) -> None:
        self.size = (width, height)

    def add_text(self, text: str, font: str, color: str) -> None:
        self.text = (text, font, color)

    def add_decorative_element(self, element: str) -> None:
        # Placeholder for adding decorative elements
        pass

    def crop_image(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            cropped_image = image.crop((x1, y1, x2, y2))
            self.image_path = cropped_image

    def resize_image(self, width: int, height: int) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            resized_image = image.resize((width, height))
            self.image_path = resized_image

    def apply_effect(self, effect: str) -> None:
        if self.image_path:
            image = Image.open(self.image_path)
            if effect == "grayscale":
                image = image.convert("L")
            self.image_path = image

    def save_as_png(self, file_name: str) -> None:
        if self.image_path:
            self.image_path.save(file_name, "PNG")

    def load_user_preferences(self) -> None:
        if os.path.exists(self.user_preferences_file):
            with open(self.user_preferences_file, 'r') as file:
                preferences = json.load(file)
                self.shape = preferences.get('shape', self.shape)
                self.size = tuple(preferences.get('size', self.size))
                self.text = preferences.get('text', self.text)

    def save_user_preferences(self) -> None:
        preferences = {
            'shape': self.shape,
            'size': self.size,
            'text': self.text
        }
        with open(self.user_preferences_file, 'w') as file:
            json.dump(preferences, file)