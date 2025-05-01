from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, file_path: str):
        self.image = Image.open(file_path)

    def crop(self, dimensions: tuple) -> Image:
        if self.image:
            return self.image.crop(dimensions)
        return None

    def resize(self, size: tuple) -> Image:
        if self.image:
            self.image = self.image.resize(size)
        return self.image

    def apply_effects(self, effect: str) -> Image:
        if self.image:
            if effect == "grayscale":
                self.image = self.image.convert("L")
        return self.image

    def get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")