import tkinter as tk
from tkinter import colorchooser, messagebox
from brush_tools import Brush
from layers import LayerManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("PaintPal")
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.toolbar = Toolbar(self)
        self.layer_manager = LayerManager()
        self.current_layer = None

    def main(self):
        self.root.mainloop()

class Toolbar:
    def __init__(self, main_app):
        self.main_app = main_app
        self.current_brush = Brush()
        self.create_toolbar()

    def create_toolbar(self):
        toolbar_frame = tk.Frame(self.main_app.root)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        brush_button = tk.Button(toolbar_frame, text="Select Brush", command=self.select_brush)
        brush_button.pack(side=tk.LEFT)

        color_button = tk.Button(toolbar_frame, text="Select Color", command=self.select_color)
        color_button.pack(side=tk.LEFT)

        size_button = tk.Button(toolbar_frame, text="Adjust Size", command=self.adjust_size)
        size_button.pack(side=tk.LEFT)

    def select_brush(self):
        # Logic to select brush
        pass

    def select_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_brush.set_color(color)

    def adjust_size(self):
        size = tk.simpledialog.askinteger("Brush Size", "Enter brush size:")
        if size:
            self.current_brush.set_size(size)

class Canvas:
    def __init__(self):
        self.layers = []

    def draw(self):
        # Drawing logic
        pass

    def save_artwork(self, filename: str):
        # Save artwork logic
        pass

    def export_artwork(self, format: str):
        # Export artwork logic
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()