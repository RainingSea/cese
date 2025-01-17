from layer_manager import LayerManager
from brush import Brush

class Canvas:
    def __init__(self):
        self.layers = LayerManager()
        self.current_brush = Brush()

    def draw(self, position: tuple, color: tuple) -> None:
        if self.layers.get_layers():
            current_layer = self.layers.get_layers()[-1]  # Draw on the top layer
            current_layer.draw_on_layer(self.current_brush, position, color)

    def clear(self) -> None:
        for layer in self.layers.get_layers():
            layer.clear_layer()

    def save_artwork(self, file_path: str) -> None:
        # Here, implement the logic to save the artwork from all layers
        # This is a placeholder for the actual saving implementation
        pass