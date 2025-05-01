import tkinter as tk
import json
from shape import Shape
from toolbar import Toolbar

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("ShapeMaster")
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.toolbar = Toolbar(self.canvas)
        self.load_shapes()

    def main(self):
        self.master.mainloop()

    def load_shapes(self):
        try:
            with open('shapes.json', 'r') as file:
                shapes_data = json.load(file)
                for shape_data in shapes_data:
                    shape = Shape(shape_data['type'], tuple(shape_data['position']),
                                  tuple(shape_data['size']), shape_data['style'])
                    shape.draw(self.canvas)
        except FileNotFoundError:
            print("Shapes file not found. Starting with an empty canvas.")

    def save_shapes(self):
        shapes = self.canvas.find_all()
        shapes_data = []
        for shape in shapes:
            shape_info = self.canvas.itemcget(shape, "type")
            position = self.canvas.coords(shape)
            size = (self.canvas.itemcget(shape, "width"), self.canvas.itemcget(shape, "height"))
            style = {"fill": self.canvas.itemcget(shape, "fill")}
            shapes_data.append({"type": shape_info, "position": position, "size": size, "style": style})
        with open('shapes.json', 'w') as file:
            json.dump(shapes_data, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()