import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Manipulation Application")
        self.canvas = Canvas(self.root)
        self.toolbar = Toolbar(self.root, self.canvas)

    def main(self):
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()