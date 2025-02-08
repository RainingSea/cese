import random

class Obstacle:
    def __init__(self, position: int, type: bool):
        self.position = position  # Position of the obstacle on the lane
        self.type = type  # True for slowing down, False for game over

    def move(self):
        # Move the obstacle down the lane
        self.position += 5  # Move down by 5 units