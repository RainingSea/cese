import random

class Obstacle:
    def __init__(self, type: int, position: int):
        self.type = type
        self.position = position

    def move(self):
        self.position += 5  # Move the obstacle down the screen