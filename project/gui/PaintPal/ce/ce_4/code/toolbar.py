from brush import Brush

class Toolbar:
    def __init__(self):
        self.selected_brush = Brush(size=5, opacity=1.0, blend_mode='normal')

    def select_brush(self, brush: Brush):
        self.selected_brush = brush

    def adjust_brush_size(self, size: int):
        self.selected_brush.size = size

    def adjust_brush_opacity(self, opacity: float):
        self.selected_brush.opacity = opacity

    def change_blend_mode(self, mode: str):
        self.selected_brush.blend_mode = mode