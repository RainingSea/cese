from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.image = None

    def import_image(self, file_path: str) -> None:
        self.image = Image.open(file_path)

    def crop_image(self, crop_area: tuple) -> None:
        if self.image:
            self.image = self.image.crop(crop_area)

    def resize_image(self, new_size: tuple) -> None:
        if self.image:
            self.image = self.image.resize(new_size)

    def apply_effect(self, effect_type: str) -> None:
        if self.image:
            if effect_type == "grayscale":
                self.image = self.image.convert("L")
            # Additional effects can be added here