import tkinter as tk
from shape_manager import ShapeManager

class Main:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("ShapeMaster")
        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()
        self.shape_manager = ShapeManager()
        self.shape_manager.load_shapes()
        self.draw_shapes()

    def draw_shapes(self) -> None:
        for shape in self.shape_manager.shapes:
            shape.draw(self.canvas)

    def main(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()