import random

class Target:
    def __init__(self):
        self.position = (random.randint(0, 800), random.randint(0, 600))
        self.speed = random.randint(1, 5)

    def move(self, speed: int) -> None:
        # Move right for simplicity
        self.position = (self.position[0] + speed, self.position[1])