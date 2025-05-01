from PIL import Image, ImageDraw

class StickerCreator:
    def __init__(self):
        self.shape = None
        self.size = (100, 100)  # Default size
        self.text = ""
        self.text_color = "black"
        self.sticker_image = None

    def select_shape(self, shape: str):
        self.shape = shape

    def set_size(self, size: tuple):
        self.size = size

    def add_text(self, text: str, color: str):
        self.text = text
        self.text_color = color

    def create_sticker(self, base_image: Image) -> Image:
        sticker_image = base_image.copy()
        draw = ImageDraw.Draw(sticker_image)
        if self.shape == "Circle":
            draw.ellipse([10, 10, 10 + self.size[0], 10 + self.size[1]], outline=self.text_color)
        elif self.shape == "Square":
            draw.rectangle([10, 10, 10 + self.size[0], 10 + self.size[1]], outline=self.text_color)
        elif self.shape == "Star":
            self.draw_star(draw, 10, 10, self.size[0] // 2, self.text_color)
        draw.text((15, 15), self.text, fill=self.text_color)
        self.sticker_image = sticker_image
        return sticker_image

    def draw_star(self, draw: ImageDraw, x: int, y: int, size: int, color: str):
        points = [
            (x, y + size),
            (x + size * 0.2245, y + size * 0.3090),
            (x + size, y + size * 0.3090),
            (x + size * 0.3633, y - size * 0.1180),
            (x + size * 0.5878, y - size * 0.8090),
            (x, y - size * 0.6180),
            (x - size * 0.5878, y - size * 0.8090),
            (x - size * 0.3633, y - size * 0.1180),
            (x - size, y + size * 0.3090),
            (x - size * 0.2245, y + size * 0.3090),
        ]
        draw.polygon(points, outline=color)

    def save_sticker(self, image: Image, filename: str):
        image.save(filename, "PNG")