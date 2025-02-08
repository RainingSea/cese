import tkinter as tk
from canvas import Canvas
from shape_manager import ShapeManager

class Main:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master)
        self.shape_manager = ShapeManager()
        self.canvas.canvas.pack(fill=tk.BOTH, expand=True)

    def main(self):
        self.load_shapes()
        self.master.mainloop()

    def load_shapes(self):
        self.shape_manager.load_shapes_from_file('shapes.json')
        for shape in self.shape_manager.shapes:
            self.canvas.draw_shape(shape)

    def save_shapes(self):
        self.shape_manager.save_shapes_to_file('shapes.json')

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()