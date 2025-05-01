from PIL import ImageDraw, ImageFont
import os

class StickerCreator:
    def __init__(self):
        self.shapes = ["Circle", "Square", "Star"]
        self.sticker_image = None

    def choose_shape(self, shape: str) -> None:
        self.shape = shape

    def add_text(self, text: str, font: str, color: str) -> None:
        if self.sticker_image:
            draw = ImageDraw.Draw(self.sticker_image)
            font = ImageFont.load_default()
            draw.text((10, 10), text, font=font, fill=color)

    def add_decorative_element(self, element: str) -> None:
        # Placeholder for adding decorative elements
        pass

    def save_sticker(self, file_path: str) -> None:
        if self.sticker_image:
            self.sticker_image.save(file_path)

    def create_sticker(self):
        # Placeholder for creating a sticker image based on chosen shape
        pass