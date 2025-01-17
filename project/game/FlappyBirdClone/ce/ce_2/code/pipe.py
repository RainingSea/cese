import random

class Pipe:
    def __init__(self, x_position: float, gap_height: float):
        self.x_position = x_position
        self.gap_height = gap_height

    def move(self) -> float:
        self.x_position -= 5  # Move pipe left
        return self.x_position

    def get_position(self) -> float:
        return self.x_position