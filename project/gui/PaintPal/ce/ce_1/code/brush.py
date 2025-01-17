class Brush:
    def __init__(self, size: int = 5, opacity: float = 1.0, blend_mode: str = "normal"):
        self.size = size
        self.opacity = opacity
        self.blend_mode = blend_mode

    def set_size(self, size: int) -> None:
        self.size = size

    def set_opacity(self, opacity: float) -> None:
        self.opacity = opacity

    def set_blend_mode(self, mode: str) -> None:
        self.blend_mode = mode