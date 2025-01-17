import tkinter as tk

class Shape:
    def __init__(self, shape_type: str, properties: dict) -> None:
        self.shape_type = shape_type
        self.properties = properties

    def draw(self, canvas: tk.Canvas) -> None:
        if self.shape_type == 'rectangle':
            canvas.create_rectangle(**self.properties)
        elif self.shape_type == 'circle':
            x, y, r = self.properties['x'], self.properties['y'], self.properties['radius']
            canvas.create_oval(x - r, y - r, x + r, y + r, **self.properties)
        elif self.shape_type == 'triangle':
            points = self.properties['points']
            canvas.create_polygon(points, **self.properties)
        elif self.shape_type == 'polygon':
            points = self.properties['points']
            canvas.create_polygon(points, **self.properties)

    def resize(self, new_size: tuple) -> None:
        self.properties['width'], self.properties['height'] = new_size

    def reposition(self, new_position: tuple) -> None:
        self.properties['x'], self.properties['y'] = new_position

    def apply_style(self, style: dict) -> None:
        self.properties.update(style)