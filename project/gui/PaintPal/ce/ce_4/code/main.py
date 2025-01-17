import tkinter as tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager

class PaintPal:
    def __init__(self):
        self.canvas = Canvas()
        self.toolbar = Toolbar()
        self.layer_manager = LayerManager()

    def main(self) -> str:
        root = tk.Tk()
        root.title("PaintPal")
        
        # Setup UI components here
        
        root.mainloop()
        return "Application closed"

if __name__ == "__main__":
    app = PaintPal()
    app.main()