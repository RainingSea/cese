import tkinter as tk
from PIL import Image, ImageDraw

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.current_brush = None
        self.current_color = "black"
        self.bind("<B1-Motion>", self.draw)
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw_image = ImageDraw.Draw(self.image)

    def draw(self, event):
        if self.current_brush is not None:
            x, y = event.x, event.y
            size = self.current_brush.size
            self.create_oval(x - size, y - size, x + size, y + size, fill=self.current_color, outline=self.current_color)
            self.draw_image.ellipse([x - size, y - size, x + size, y + size], fill=self.current_color)

    def save_artwork(self, filename: str):
        self.image.save(filename)