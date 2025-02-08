from PIL import Image, ImageEnhance, ImageFilter

class ImageEditor:
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
            elif filter_type == "DETAIL":
                self.image = self.image.filter(ImageFilter.DETAIL)
            elif filter_type == "EDGE_ENHANCE":
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == "EMBOSS":
                self.image = self.image.filter(ImageFilter.EMBOSS)

    def apply_effect(self, effect_type: str) -> None:
        # For simplicity, let's assume effects are similar to filters
        self.apply_filter(effect_type)

    def crop_image(self, left: int, upper: int, right: int, lower: int) -> None:
        if self.image is not None:
            self.image = self.image.crop((left, upper, right, lower))

    def resize_image(self, width: int, height: int) -> None:
        if self.image is not None:
            self.image = self.image.resize((width, height))

    def save_image(self, file_path: str) -> None:
        if self.image is not None:
            self.image.save(file_path)