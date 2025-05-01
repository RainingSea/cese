from PIL import ImageEnhance, ImageFilter

class ImageProcessor:
    def __init__(self):
        self.image = None

    def import_image(self, file_path: str) -> None:
        self.image = Image.open(file_path)

    def adjust_brightness(self, value: int) -> None:
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(value)

    def adjust_contrast(self, value: int) -> None:
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(value)

    def adjust_saturation(self, value: int) -> None:
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(value)

    def apply_filter(self, filter_type: str) -> None:
        if filter_type == "BLUR":
            self.image = self.image.filter(ImageFilter.BLUR)
        elif filter_type == "CONTOUR":
            self.image = self.image.filter(ImageFilter.CONTOUR)

    def crop(self, x: int, y: int, width: int, height: int) -> None:
        self.image = self.image.crop((x, y, x + width, y + height))

    def resize(self, width: int, height: int) -> None:
        self.image = self.image.resize((width, height))

    def save_image(self, file_path: str) -> None:
        self.image.save(file_path)