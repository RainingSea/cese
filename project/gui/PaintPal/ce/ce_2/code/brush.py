class Brush:
    def __init__(self, size: int, opacity: float, blend_mode: str):
        self.size = size
        self.opacity = opacity
        self.blend_mode = blend_mode

    def set_size(self, size: int):
        self.size = size

    def set_opacity(self, opacity: float):
        self.opacity = opacity

    def set_blend_mode(self, blend_mode: str):
        self.blend_mode = blend_mode