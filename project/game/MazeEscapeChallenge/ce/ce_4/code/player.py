class Player:
    def __init__(self, start_position: tuple):
        self.position = start_position
        self.time_taken = 0.0

    def move(self, direction: str) -> None:
        if direction == 'up':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'down':
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == 'left':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'right':
            self.position = (self.position[0], self.position[1] + 1)

    def set_time(self, time: float) -> None:
        self.time_taken = time