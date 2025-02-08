import tkinter as tk
from PIL import Image, ImageDraw
from layer import Layer

class Canvas:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack()
        self.layers = []
        self.current_brush = None
        self.image = Image.new('RGB', (800, 600), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

    def draw_on_canvas(self, event):
        if self.current_brush:
            x, y = event.x, event.y
            self.draw.line((x, y, x + self.current_brush.size, y + self.current_brush.size), fill=self.current_brush.color)
            self.canvas.create_line(x, y, x + self.current_brush.size, y + self.current_brush.size, fill=self.current_brush.color)

    def save_artwork(self, file_path: str):
        self.image.save(file_path)

    def load_artwork(self, file_path: str):
        self.image = Image.open(file_path)
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def set_brush(self, brush):
        self.current_brush = brush