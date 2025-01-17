import tkinter as tk
from shape_manager import ShapeManager

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShapeMaster")
        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()
        self.shape_manager = ShapeManager()
        self.create_ui()

    def create_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Shape buttons
        tk.Button(toolbar, text="Rectangle", command=lambda: self.create_shape('rectangle')).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Circle", command=lambda: self.create_shape('circle')).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Triangle", command=lambda: self.create_shape('triangle')).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Polygon", command=lambda: self.create_shape('polygon')).pack(side=tk.LEFT)

        # Save and Load buttons
        tk.Button(toolbar, text="Save", command=self.save_shapes).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Load", command=self.load_shapes).pack(side=tk.LEFT)

    def create_shape(self, shape_type):
        # Example position and size, real implementation should get user input
        position = (100, 100)
        size = (50, 50)
        style = {'fill': 'blue', 'outline': 'black'}
        shape = self.shape_manager.create_shape(shape_type, position, size, style)
        shape.draw(self.canvas)

    def save_shapes(self):
        self.shape_manager.save_shapes_to_file('shapes.json')

    def load_shapes(self):
        self.shape_manager.load_shapes_from_file('shapes.json')
        self.canvas.delete("all")  # Clear canvas before redrawing
        for shape in self.shape_manager.shapes:
            shape.draw(self.canvas)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()