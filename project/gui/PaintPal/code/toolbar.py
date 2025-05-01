import tkinter as tk
from brush import Brush
from color_palette import ColorPalette

class Toolbar(tk.Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        self.current_brush = Brush()
        self.current_palette = ColorPalette()
        self.canvas = canvas
        self.create_widgets()

    def create_widgets(self):
        self.brush_size_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, command=self.adjust_size)
        self.brush_size_slider.pack(side=tk.LEFT)

        self.opacity_slider = tk.Scale(self, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self.adjust_opacity)
        self.opacity_slider.pack(side=tk.LEFT)

        self.blend_mode_dropdown = tk.StringVar(self)
        self.blend_mode_dropdown.set("Normal")
        self.blend_mode_menu = tk.OptionMenu(self, self.blend_mode_dropdown, "Normal", "Multiply", "Screen", command=self.change_blend_mode)
        self.blend_mode_menu.pack(side=tk.LEFT)

        self.brush_selection = tk.StringVar(self)
        self.brush_selection.set("Select Brush")
        self.brush_menu = tk.OptionMenu(self, self.brush_selection, "Round", "Square", "Custom", command=self.select_brush)
        self.brush_menu.pack(side=tk.LEFT)

    def select_brush(self, brush_type: str):
        if brush_type == "Round":
            self.current_brush = Brush(size=self.brush_size_slider.get())
        elif brush_type == "Square":
            self.current_brush = Brush(size=self.brush_size_slider.get(), blend_mode="Square")
        elif brush_type == "Custom":
            # Logic for custom brush selection can be added here
            pass

    def adjust_size(self, size: int):
        self.current_brush.set_size(int(size))

    def adjust_opacity(self, opacity: float):
        self.current_brush.set_opacity(float(opacity))

    def change_blend_mode(self, mode: str):
        self.current_brush.set_blend_mode(mode)