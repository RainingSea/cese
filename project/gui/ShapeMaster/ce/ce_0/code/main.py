import tkinter as tk
from shape_master import ShapeMaster

class ShapeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Geometric Shapes")
        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack()

        self.toolbar = tk.Frame(master)
        self.toolbar.pack()

        self.shape_master = ShapeMaster()
        self.shape_master.load_shapes()

        self.create_buttons()

    def create_buttons(self):
        rectangle_button = tk.Button(self.toolbar, text="Add Rectangle", command=self.add_rectangle)
        rectangle_button.pack(side=tk.LEFT)

        circle_button = tk.Button(self.toolbar, text="Add Circle", command=self.add_circle)
        circle_button.pack(side=tk.LEFT)

        save_button = tk.Button(self.toolbar, text="Save Shapes", command=self.save_shapes)
        save_button.pack(side=tk.LEFT)

    def add_rectangle(self):
        self.shape_master.create_shape("rectangle", (50, 50), (100, 50), {"fill": "blue"})
        self.redraw_shapes()

    def add_circle(self):
        self.shape_master.create_shape("circle", (200, 200), (50, 50), {"fill": "red"})
        self.redraw_shapes()

    def redraw_shapes(self):
        self.canvas.delete("all")
        for shape in self.shape_master._shapes:
            shape.draw(self.canvas)

    def save_shapes(self):
        self.shape_master.save_shapes()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeApp(root)
    root.mainloop()