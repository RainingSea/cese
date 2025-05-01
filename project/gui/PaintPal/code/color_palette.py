class ColorPalette:
    def __init__(self):
        self.colors = ["#FFFFFF", "#000000", "#FF0000", "#00FF00", "#0000FF"]

    def select_color(self, index: int):
        return self.colors[index] if 0 <= index < len(self.colors) else None