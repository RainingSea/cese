import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager

class PaintPal:
    def __init__(self):
        self.canvas = Canvas()
        self.toolbar = Toolbar()
        self.layer_manager = LayerManager()

    def run(self) -> None:
        root = tk.Tk()
        root.title("PaintPal")
        
        # Set up the UI components here (canvas, toolbar, etc.)
        # This is a placeholder for the actual UI setup
        root.mainloop()

if __name__ == "__main__":
    app = PaintPal()
    app.run()