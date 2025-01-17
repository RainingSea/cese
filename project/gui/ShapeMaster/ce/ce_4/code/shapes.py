class Shape:
    def __init__(self, shape_type: str, position: tuple, size: tuple, style: dict):
        self.type = shape_type
        self.position = position
        self.size = size
        self.style = style


class Group:
    def __init__(self, shapes: list):
        self.shapes = shapes