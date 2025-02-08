class Player:
    def __init__(self):
        self.position = (0, 0)

    def move(self, direction: str) -> None:
        x, y = self.position
        if direction == 'up':
            self.position = (x, y - 1)
        elif direction == 'down':
            self.position = (x, y + 1)
        elif direction == 'left':
            self.position = (x - 1, y)
        elif direction == 'right':
            self.position = (x + 1, y)

    def get_position(self) -> tuple:
        return self.position