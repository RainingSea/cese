from brush import Brush

class Toolbar:
    def __init__(self):
        self.brush_selector = None  # Placeholder for BrushSelector
        self.color_palette = None    # Placeholder for ColorPalette
        self.current_brush = Brush()

    def select_brush(self, brush: Brush) -> None:
        self.current_brush = brush

    def select_color(self, color: str) -> None:
        # Implement color selection logic
        pass

    def adjust_size(self, size: int) -> None:
        self.current_brush.set_size(size)

    def adjust_opacity(self, opacity: float) -> None:
        self.current_brush.set_opacity(opacity)

    def change_blend_mode(self, mode: str) -> None:
        self.current_brush.set_blend_mode(mode)