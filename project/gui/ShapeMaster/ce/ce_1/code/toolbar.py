import tkinter as tk
from canvas import Canvas

class Toolbar(tk.Frame):
    def __init__(self, master, canvas: Canvas):
        super().__init__(master)
        self.canvas = canvas
        self.create_widgets()

    def create_widgets(self):
        self.rectangle_button = tk.Button(self, text="Rectangle", command=lambda: self.create_shape("rectangle"))
        self.rectangle_button.pack(fill=tk.X)

        self.circle_button = tk.Button(self, text="Circle", command=lambda: self.create_shape("circle"))
        self.circle_button.pack(fill=tk.X)

        # Add additional shape buttons as needed

    def create_shape(self, shape_type: str):
        # Example shape creation logic
        if shape_type == "rectangle":
            shape = Shape("rectangle", [50, 50, 150, 100], None)  # Example properties
            self.canvas.shapes.append(shape)
            self.canvas.draw_shape(shape)
        elif shape_type == "circle":
            shape = Shape("circle", [200, 50, 300, 150], None)  # Example properties
            self.canvas.shapes.append(shape)
            self.canvas.draw_shape(shape)