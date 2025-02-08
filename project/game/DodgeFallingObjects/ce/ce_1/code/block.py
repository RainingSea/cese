import random

class Block:
    def __init__(self, x: int, speed: int):
        self.x_position = x
        self.y_position = 0
        self.speed = speed

    def fall(self) -> None:
        self.y_position += self.speed

    def get_position(self) -> tuple:
        return (self.x_position, self.y_position)