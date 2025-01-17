from PIL import Image, ImageEnhance, ImageFilter

class Effects:
    """Class to define various image effects."""
    
    @staticmethod
    def apply_blur(image: Image) -> Image:
        """Apply blur effect to the image."""
        return image.filter(ImageFilter.BLUR)

    @staticmethod
    def apply_sharpen(image: Image) -> Image:
        """Apply sharpen effect to the image."""
        return image.filter(ImageFilter.SHARPEN)

    @staticmethod
    def apply_brightness(image: Image, factor: float) -> Image:
        """Adjust brightness of the image."""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_contrast(image: Image, factor: float) -> Image:
        """Adjust contrast of the image."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)