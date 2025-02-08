from brush import Brush
from color_palette import ColorPalette

class Toolbar:
    def __init__(self):
        self.brushes = [Brush(size) for size in range(1, 11)]
        self.color_palette = ColorPalette()

    def select_brush(self, brush: Brush) -> None:
        self.current_brush = brush

    def adjust_size(self, size: int) -> None:
        self.current_brush.set_size(size)

    def adjust_opacity(self, opacity: float) -> None:
        self.current_brush.set_opacity(opacity)

    def change_blend_mode(self, mode: str) -> None:
        self.current_brush.set_blend_mode(mode)