class Player:
    def __init__(self, start_position: tuple):
        self.position = start_position
        self.completion_time = 0.0

    def move(self, direction: str) -> None:
        x, y = self.position
        if direction == 'up':
            self.position = (x - 1, y)
        elif direction == 'down':
            self.position = (x + 1, y)
        elif direction == 'left':
            self.position = (x, y - 1)
        elif direction == 'right':
            self.position = (x, y + 1)

    def reach_exit(self) -> None:
        self.completion_time = time.time() - self.start_time