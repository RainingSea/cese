import random

class Block:
    def __init__(self, size: int):
        self.size = size
        self.x_position = random.randint(0, 800 - size)  # Assuming screen width is 800
        self.y_position = 0

    def fall(self, speed: int) -> None:
        self.y_position += speed

    def get_position(self) -> tuple:
        return (self.x_position, self.y_position)