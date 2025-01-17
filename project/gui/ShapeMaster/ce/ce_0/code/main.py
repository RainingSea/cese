from tkinter import Tk
from canvas import Canvas
from data_storage import load_shapes, load_preferences

class Main:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas()
        self.initialize()

    def initialize(self):
        shapes = load_shapes()
        preferences = load_preferences()
        for shape in shapes:
            self.canvas.draw_shape(shape)

    def main(self) -> str:
        self.root.mainloop()
        return "Application closed"

if __name__ == "__main__":
    app = Main()
    app.main()