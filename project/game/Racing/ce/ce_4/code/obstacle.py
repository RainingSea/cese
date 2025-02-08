import random

class Obstacle:
    def __init__(self, type: int, position: int):
        self.type = type
        self.position = position

    def move(self):
        self.position += 5  # Move the obstacle down the lane

    def check_collision(self, car_position: int) -> bool:
        # Simple collision detection based on position
        return self.position >= car_position and self.position <= car_position + 50  # Assuming car width is 50