class Color:
    def __init__(self, name: str, hex_value: str):
        self.name = name
        self.hex_value = hex_value

class ColorPalette:
    def __init__(self):
        self.colors = []

    def select_color(self, color: Color) -> None:
        # This method would handle the selection of the color
        pass

    def add_color(self, color: Color) -> None:
        self.colors.append(color)