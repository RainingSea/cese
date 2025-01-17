class ColorPalette:
    def __init__(self):
        self.colors = []

    def select_color(self, color: str) -> None:
        if color not in self.colors:
            self.colors.append(color)