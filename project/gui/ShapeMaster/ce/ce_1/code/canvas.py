import tkinter as tk
import json
from shapes import Shape

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.shapes = []
        self.bind("<Button-1>", self.on_click)

    def draw_shape(self, shape: Shape):
        if shape.type == "rectangle":
            self.create_rectangle(shape.properties[0], shape.properties[1], shape.properties[2], shape.properties[3], fill=shape.style.color)
        elif shape.type == "circle":
            self.create_oval(shape.properties[0], shape.properties[1], shape.properties[2], shape.properties[3], fill=shape.style.color)
        # Add additional shape types as needed

    def edit_shape(self, shape: Shape):
        # Implement shape editing logic
        pass

    def load_shapes(self):
        try:
            with open('shapes.json', 'r') as file:
                data = json.load(file)
                for shape_data in data:
                    shape = Shape(shape_data['type'], shape_data['properties'], shape_data['style'])
                    self.shapes.append(shape)
                    self.draw_shape(shape)
        except FileNotFoundError:
            print("No shapes file found.")

    def save_shapes(self):
        with open('shapes.json', 'w') as file:
            json.dump([shape.__dict__ for shape in self.shapes], file)

    def on_click(self, event):
        # Example click handler
        print(f"Clicked at: {event.x}, {event.y}")