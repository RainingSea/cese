import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("PaintPal")
        self.canvas = Canvas(self.root)
        self.toolbar = Toolbar(self.root, self.canvas)
        self.layer_manager = LayerManager(self.root, self.canvas)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()