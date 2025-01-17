import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager
import json
import os

class PaintPal:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = Canvas()
        self.toolbar = Toolbar()
        self.layer_manager = LayerManager()
        self.load_settings()

    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                self.toolbar.adjust_size(settings.get('brush_size', 5))
                self.toolbar.adjust_opacity(settings.get('brush_opacity', 1.0))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintPal()
    app.run()