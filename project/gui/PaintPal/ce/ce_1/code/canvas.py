from PIL import Image, ImageDraw
from brush import Brush
from layer_manager import LayerManager

class Canvas:
    def __init__(self):
        self.layers = LayerManager()
        self.current_brush = Brush()
        self.image = Image.new("RGBA", (800, 600), (255, 255, 255, 0))

    def draw(self, position: tuple) -> None:
        if self.layers.get_layers():
            draw = ImageDraw.Draw(self.image)
            x, y = position
            draw.ellipse((x - self.current_brush.size, y - self.current_brush.size,
                           x + self.current_brush.size, y + self.current_brush.size),
                           fill=(0, 0, 0, int(255 * self.current_brush.opacity)))

    def save_artwork(self, filename: str) -> None:
        self.image.save(filename, "PNG")