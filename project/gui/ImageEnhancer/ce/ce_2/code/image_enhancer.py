from PIL import Image, ImageEnhance, ImageFilter

class ImageEnhancer:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = self.load_image()

    def load_image(self) -> Image.Image:
        """Load an image from the specified path."""
        return Image.open(self.image_path)

    def adjust_brightness(self, value: float) -> None:
        """Adjust the brightness of the image."""
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(value)

    def adjust_contrast(self, value: float) -> None:
        """Adjust the contrast of the image."""
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(value)

    def adjust_saturation(self, value: float) -> None:
        """Adjust the saturation of the image."""
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(value)

    def apply_filter(self, filter_type: str) -> None:
        """Apply a filter to the image."""
        if filter_type == 'BLUR':
            self.image = self.image.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        elif filter_type == 'DETAIL':
            self.image = self.image.filter(ImageFilter.DETAIL)
        elif filter_type == 'EDGE_ENHANCE':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'EMBOSS':
            self.image = self.image.filter(ImageFilter.EMBOSS)

    def crop_image(self, left: int, upper: int, right: int, lower: int) -> None:
        """Crop the image to the specified box."""
        self.image = self.image.crop((left, upper, right, lower))

    def resize_image(self, width: int, height: int) -> None:
        """Resize the image to the specified dimensions."""
        self.image = self.image.resize((width, height))

    def save_image(self, output_path: str) -> None:
        """Save the enhanced image to the specified path."""
        self.image.save(output_path)