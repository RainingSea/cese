class Player:
    def __init__(self):
        self.position = (0, 1)  # Starting position

    def move(self, direction: str):
        x, y = self.position
        if direction == 'up':
            self.position = (max(0, x - 1), y)
        elif direction == 'down':
            self.position = (min(9, x + 1), y)
        elif direction == 'left':
            self.position = (x, max(0, y - 1))
        elif direction == 'right':
            self.position = (x, min(9, y + 1))

    def check_exit(self) -> bool:
        return self.position == (9, 8)  # Exit position