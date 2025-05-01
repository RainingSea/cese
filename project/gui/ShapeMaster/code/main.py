import tkinter as tk
from tkinter import colorchooser, filedialog
import json
from shape import Shape
from shape_manager import ShapeManager

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.shape_manager = ShapeManager()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.create_ui()

    def create_ui(self):
        tk.Button(self.root, text="Add Rectangle", command=self.add_rectangle).pack()
        tk.Button(self.root, text="Add Circle", command=self.add_circle).pack()
        tk.Button(self.root, text="Add Triangle", command=self.add_triangle).pack()
        tk.Button(self.root, text="Add Polygon", command=self.add_polygon).pack()
        tk.Button(self.root, text="Save Shapes", command=self.shape_manager.save_shapes).pack()
        tk.Button(self.root, text="Load Shapes", command=self.load_shapes).pack()
        tk.Button(self.root, text="Align Left", command=lambda: self.shape_manager.align_shapes('left')).pack()
        tk.Button(self.root, text="Align Center", command=lambda: self.shape_manager.align_shapes('center')).pack()
        tk.Button(self.root, text="Align Right", command=lambda: self.shape_manager.align_shapes('right')).pack()

    def add_rectangle(self):
        attributes = {'position': (50, 50), 'size': (100, 50), 'style': {'color': 'blue'}}
        shape = self.shape_manager.create_shape('rectangle', **attributes)
        shape.draw(self.canvas)

    def add_circle(self):
        attributes = {'position': (200, 200), 'size': (50,), 'style': {'color': 'red'}}
        shape = self.shape_manager.create_shape('circle', **attributes)
        shape.draw(self.canvas)

    def add_triangle(self):
        attributes = {'position': (300, 300), 'size': (100, 80), 'style': {'color': 'green'}}
        shape = self.shape_manager.create_shape('triangle', **attributes)
        shape.draw(self.canvas)

    def add_polygon(self):
        attributes = {'position': (400, 400), 'size': {'points': [400, 400, 450, 450, 350, 450]}, 'style': {'color': 'orange'}}
        shape = self.shape_manager.create_shape('polygon', **attributes)
        shape.draw(self.canvas)

    def load_shapes(self):
        self.shape_manager.load_shapes()
        self.redraw_shapes()

    def redraw_shapes(self):
        self.canvas.delete("all")
        for shape in self.shape_manager.shapes:
            shape.draw(self.canvas)

    def main(self):
        self.load_shapes()
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()