import tkinter as tk

class Shape:
    def __init__(self, shape_type, position, size, style):
        self.type = shape_type
        self.position = position
        self.size = size
        self.style = style

    def draw(self, canvas):
        if self.type == "rectangle":
            canvas.create_rectangle(*self.position, self.position[0] + self.size[0], 
                                    self.position[1] + self.size[1], fill=self.style.get("fill", "black"))
        elif self.type == "circle":
            canvas.create_oval(*self.position, self.position[0] + self.size[0], 
                               self.position[1] + self.size[1], fill=self.style.get("fill", "black"))
        elif self.type == "triangle":
            x1, y1 = self.position
            x2, y2 = self.position[0] + self.size[0], self.position[1]
            x3, y3 = self.position[0] + self.size[0] / 2, self.position[1] - self.size[1]
            canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=self.style.get("fill", "black"))
        # Additional shape types can be added here

    def resize(self, new_size):
        self.size = new_size

    def reposition(self, new_position):
        self.position = new_position

    def apply_style(self, new_style):
        self.style.update(new_style)