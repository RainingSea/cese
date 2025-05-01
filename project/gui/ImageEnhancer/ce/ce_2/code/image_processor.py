from PIL import Image, ImageTk, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.image_path = ""

    def load_image(self, file_path: str) -> None:
        self.image_path = file_path
        self.image = Image.open(file_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

    def adjust_brightness(self, value: float) -> None:
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def adjust_contrast(self, value: float) -> None:
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def adjust_saturation(self, value: float) -> None:
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def apply_filter(self, filter_name: str) -> None:
        if filter_name == "BLUR":
            self.image = self.image.filter(ImageFilter.BLUR)
        elif filter_name == "CONTOUR":
            self.image = self.image.filter(ImageFilter.CONTOUR)

    def crop_image(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        self.image = self.image.crop((start_x, start_y, end_x, end_y))

    def resize_image(self, width: int, height: int) -> None:
        self.image = self.image.resize((width, height))

    def save_image(self, file_name: str) -> None:
        self.image.save(file_name)