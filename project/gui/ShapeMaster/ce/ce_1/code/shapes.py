class Shape:
    def __init__(self, shape_type: str, properties: list, style):
        self.type = shape_type
        self.properties = properties
        self.style = style

    def set_style(self, style):
        self.style = style