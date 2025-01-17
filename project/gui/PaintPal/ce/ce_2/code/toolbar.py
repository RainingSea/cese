import tkinter as tk
from brush import Brush
from color_palette import ColorPalette

class Toolbar:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.toolbar_frame = tk.Frame(root)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        self.brushes = [Brush(size=5, opacity=1.0, blend_mode='normal')]
        self.color_palette = ColorPalette()

        self.create_toolbar()

    def create_toolbar(self):
        brush_button = tk.Button(self.toolbar_frame, text="Select Brush", command=self.select_brush)
        brush_button.pack(side=tk.LEFT)

        color_button = tk.Button(self.toolbar_frame, text="Select Color", command=self.select_color)
        color_button.pack(side=tk.LEFT)

    def select_brush(self):
        # In a real application, this would open a brush selection dialog
        self.canvas.set_brush(self.brushes[0])

    def select_color(self):
        # In a real application, this would open a color selection dialog
        self.canvas.current_brush.color = 'black'