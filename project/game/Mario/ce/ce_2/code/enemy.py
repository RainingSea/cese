class Enemy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self):
        self.x += 2  # Simplified movement logic