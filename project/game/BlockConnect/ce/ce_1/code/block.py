class Block:
    def __init__(self, color=None):
        self.color = color if color else self.random_color()

    def random_color(self):
        # Logic to generate a random color
        return "red"  # Placeholder

    def get_color(self):
        return self.color