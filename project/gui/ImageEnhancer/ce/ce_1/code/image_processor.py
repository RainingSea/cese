from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, file_path: str) -> None:
        self.image = Image.open(file_path)

    def adjust_brightness(self, value: float) -> None:
        if self.image is not None:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(value)

    def adjust_contrast(self, value: float) -> None:
        if self.image is not None:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(value)

    def adjust_saturation(self, value: float) -> None:
        if self.image is not None:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(value)

    def apply_filter(self, filter_type: str) -> None:
        if self.image is not None:
            if filter_type == "BLUR":
                self.image = self.image.filter(ImageFilter.BLUR)
            elif filter_type == "CONTOUR":
                self.image = self.image.filter(ImageFilter.CONTOUR)

    def apply_effect(self, effect_type: str) -> None:
        if self.image is not None:
            if effect_type == "GRAYSCALE":
                self.image = self.image.convert("L")

    def crop_image(self, left: int, top: int, right: int, bottom: int) -> None:
        if self.image is not None:
            self.image = self.image.crop((left, top, right, bottom))

    def resize_image(self, width: int, height: int) -> None:
        if self.image is not None:
            self.image = self.image.resize((width, height))

    def save_image(self, file_path: str) -> None:
        if self.image is not None:
            self.image.save(file_path)