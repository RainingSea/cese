import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PaintPal")
        self.canvas = Canvas(self.root)
        self.toolbar = Toolbar(self.root, self.canvas)
        self.layer_manager = LayerManager(self.root, self.canvas)

    def main(self):
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.layer_manager.pack(side=tk.RIGHT, fill=tk.Y)
        self.root.mainloop()

    def save_artwork(self, file_path: str):
        self.canvas.save_artwork(file_path)

if __name__ == "__main__":
    app = Main()
    app.main()