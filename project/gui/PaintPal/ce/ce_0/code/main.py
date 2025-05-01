import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("PaintPal")
        self.canvas = Canvas(self.master)
        self.toolbar = Toolbar(self.master, self.canvas)
        self.layer_manager = LayerManager(self.master)

    def main(self):
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.layer_manager.pack(side=tk.RIGHT, fill=tk.Y)
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()