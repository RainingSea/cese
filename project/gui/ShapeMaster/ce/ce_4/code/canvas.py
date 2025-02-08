import tkinter as tk
from shapes import Shape

class Canvas:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, bg='white')
        self.shapes = []

    def draw_shape(self, shape: Shape):
        if shape.type == 'rectangle':
            x0, y0 = shape.position
            x1, y1 = x0 + shape.size[0], y0 + shape.size[1]
            self.canvas.create_rectangle(x0, y0, x1, y1, **shape.style)
        elif shape.type == 'circle':
            x0, y0 = shape.position
            x1, y1 = x0 + shape.size[0], y0 + shape.size[0]
            self.canvas.create_oval(x0, y0, x1, y1, **shape.style)
        elif shape.type == 'triangle':
            x0, y0 = shape.position
            x1, y1 = x0 + shape.size[0], y0
            x2, y2 = x0 + shape.size[0] / 2, y0 + shape.size[1]
            self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, **shape.style)
        elif shape.type == 'polygon':
            x0, y0 = shape.position
            points = shape.size  # Assume size holds the points for the polygon
            self.canvas.create_polygon(points, **shape.style)

    def clear(self):
        self.canvas.delete("all")
        self.shapes.clear()