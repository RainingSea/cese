from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, path: str) -> None:
        self.image = Image.open(path)

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
            # Add more filters as needed

    def apply_effect(self, effect_type: str) -> None:
        if self.image is not None:
            # Placeholder for effect application logic
            pass

    def crop(self, x: int, y: int, width: int, height: int) -> None:
        if self.image is not None:
            self.image = self.image.crop((x, y, x + width, y + height))

    def resize(self, width: int, height: int) -> None:
        if self.image is not None:
            self.image = self.image.resize((width, height))

    def save(self, path: str) -> None:
        if self.image is not None:
            self.image.save(path, format='PNG')