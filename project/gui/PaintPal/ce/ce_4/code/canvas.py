from PIL import Image
from layer import Layer
from brush import Brush

class Canvas:
    def __init__(self):
        self.layers = []
        self.current_brush = Brush(size=5, opacity=1.0, blend_mode='normal')

    def draw(self):
        # Logic for drawing on the canvas would go here
        pass

    def save_artwork(self, file_path: str):
        # Logic to save the artwork as a PNG file
        if self.layers:
            merged_image = self.layers[0].merge()  # Simplified for demonstration
            merged_image.save(file_path)