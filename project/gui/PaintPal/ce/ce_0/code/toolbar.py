import tkinter as tk
from brush import Brush

class Toolbar(tk.Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        self.canvas = canvas
        self.brushes = [Brush(size=5, opacity=1.0, blend_mode="normal")]
        self.current_brush = self.brushes[0]
        self.create_widgets()

    def create_widgets(self):
        self.brush_size_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, label="Brush Size", command=self.adjust_size)
        self.brush_size_slider.set(self.current_brush.size)
        self.brush_size_slider.pack(side=tk.LEFT)

        self.opacity_slider = tk.Scale(self, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Opacity", command=self.adjust_opacity)
        self.opacity_slider.set(self.current_brush.opacity)
        self.opacity_slider.pack(side=tk.LEFT)

    def select_brush(self, brush: Brush):
        self.current_brush = brush
        self.canvas.current_brush = self.current_brush

    def adjust_size(self, size: int):
        self.current_brush.set_size(int(size))

    def adjust_opacity(self, opacity: float):
        self.current_brush.set_opacity(float(opacity))