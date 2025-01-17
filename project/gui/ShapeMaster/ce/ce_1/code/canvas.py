import tkinter as tk
from shapes import Shape

class Canvas:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def draw_shape(self, shape: Shape):
        if shape.type == 'rectangle':
            self.canvas.create_rectangle(**shape.properties)
        elif shape.type == 'circle':
            x, y, r = shape.properties['x'], shape.properties['y'], shape.properties['radius']
            self.canvas.create_oval(x - r, y - r, x + r, y + r)
        elif shape.type == 'triangle':
            x1, y1, x2, y2, x3, y3 = shape.properties['points']
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=shape.properties.get('fill', ''))
        elif shape.type == 'polygon':
            points = shape.properties['points']
            self.canvas.create_polygon(*points, fill=shape.properties.get('fill', ''))

    def clear_canvas(self):
        self.canvas.delete("all")