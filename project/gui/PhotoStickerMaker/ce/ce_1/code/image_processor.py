from PIL import Image

class ImageProcessor:
    def crop(self, image: Image, x: int, y: int, width: int, height: int) -> Image:
        return image.crop((x, y, x + width, y + height))

    def resize(self, image: Image, new_width: int, new_height: int) -> Image:
        return image.resize((new_width, new_height), Image.ANTIALIAS)

    def apply_effect(self, image: Image, effect: str) -> Image:
        if effect == "grayscale":
            return image.convert("L")
        elif effect == "invert":
            return Image.eval(image, lambda p: 255 - p)
        else:
            return image