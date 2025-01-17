import tkinter as tk
from canvas import Canvas
from shapes import ShapeManager

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShapeMaster")
        self.canvas = Canvas(self.root)
        self.shape_manager = ShapeManager()
        self.load_shapes('shapes.json')

    def run(self):
        self.root.mainloop()

    def load_shapes(self, file_path: str):
        self.shape_manager.load_shapes(file_path)
        for shape in self.shape_manager.get_shapes():
            self.canvas.draw_shape(shape)

if __name__ == "__main__":
    app = MainApp()
    app.run()