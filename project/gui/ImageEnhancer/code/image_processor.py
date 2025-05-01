from PIL import Image, ImageTk, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.file_path = ""

    def load_image(self, file_path: str):
        self.image = Image.open(file_path)
        self.file_path = file_path

    def save_image(self, file_path: str):
        if self.image:
            self.image.save(file_path)

    def adjust_brightness(self, value: float):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1 + value / 100)

    def adjust_contrast(self, value: float):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1 + value / 100)

    def adjust_saturation(self, value: float):
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(1 + value / 100)

    def get_tk_image(self):
        return ImageTk.PhotoImage(self.image)

    def crop(self, start_x: int, start_y: int, end_x: int, end_y: int):
        if self.image:
            self.image = self.image.crop((start_x, start_y, end_x, end_y))

    def resize(self, width: int, height: int):
        if self.image:
            self.image = self.image.resize((width, height))