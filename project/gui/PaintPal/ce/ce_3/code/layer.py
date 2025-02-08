from PIL import Image

class Layer:
    def __init__(self, name: str):
        self.name = name
        self.image = Image.new('RGBA', (800, 600), (255, 255, 255, 0))  # Transparent background

    def draw_on_layer(self, brush: 'Brush', position: tuple, color: tuple) -> None:
        # Here, you would implement the drawing logic using Pillow
        # This is a placeholder for the actual drawing implementation
        pass

    def clear_layer(self) -> None:
        self.image = Image.new('RGBA', (800, 600), (255, 255, 255, 0))  # Reset to transparent