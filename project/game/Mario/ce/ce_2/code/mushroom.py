class Mushroom:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def fall(self):
        self.y += 5  # Simplified falling logic