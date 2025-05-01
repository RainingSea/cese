import tkinter as tk
from PIL import Image, ImageDraw
from layer import Layer

class Canvas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.layers = []
        self.current_layer = None
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        if self.current_layer:
            x, y = event.x, event.y
            self.current_layer.draw(x, y)

    def save_artwork(self, file_path: str):
        if self.layers:
            image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), "white")
            draw = ImageDraw.Draw(image)
            for layer in self.layers:
                layer.draw_on_image(draw)
            image.save(file_path)

    def add_layer(self, layer: Layer):
        self.layers.append(layer)
        self.current_layer = layer