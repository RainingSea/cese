from PIL import Image, ImageEnhance, ImageFilter

class ImageEnhancer:
    def __init__(self):
        self.current_image_path = ""
        self.original_image = None
        self.edited_image = None

    def import_image(self, path: str) -> None:
        self.current_image_path = path
        self.original_image = Image.open(path)
        self.edited_image = self.original_image.copy()

    def adjust_brightness(self, value: float) -> None:
        enhancer = ImageEnhance.Brightness(self.edited_image)
        self.edited_image = enhancer.enhance(value)

    def adjust_contrast(self, value: float) -> None:
        enhancer = ImageEnhance.Contrast(self.edited_image)
        self.edited_image = enhancer.enhance(value)

    def adjust_saturation(self, value: float) -> None:
        enhancer = ImageEnhance.Color(self.edited_image)
        self.edited_image = enhancer.enhance(value)

    def apply_filter(self, filter_type: str) -> None:
        if filter_type == "BLUR":
            self.edited_image = self.edited_image.filter(ImageFilter.BLUR)
        elif filter_type == "CONTOUR":
            self.edited_image = self.edited_image.filter(ImageFilter.CONTOUR)
        elif filter_type == "DETAIL":
            self.edited_image = self.edited_image.filter(ImageFilter.DETAIL)

    def apply_effect(self, effect_type: str) -> None:
        if effect_type == "GRAYSCALE":
            self.edited_image = self.edited_image.convert("L")
        elif effect_type == "SEPIA":
            sepia_filter = Image.new("RGB", self.edited_image.size)
            for x in range(self.edited_image.width):
                for y in range(self.edited_image.height):
                    r, g, b = self.edited_image.getpixel((x, y))
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    sepia_filter.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
            self.edited_image = sepia_filter

    def crop_image(self, coordinates: tuple) -> None:
        self.edited_image = self.edited_image.crop(coordinates)

    def resize_image(self, size: tuple) -> None:
        self.edited_image = self.edited_image.resize(size)

    def save_image(self, save_path: str) -> None:
        self.edited_image.save(save_path, format='PNG')