class ColorPalette:
    def __init__(self):
        self.colors = []

    def add_color(self, color: str):
        self.colors.append(color)

    def remove_color(self, color: str):
        if color in self.colors:
            self.colors.remove(color)