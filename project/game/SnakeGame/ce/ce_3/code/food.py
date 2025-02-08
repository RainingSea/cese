import random

class Food:
    def __init__(self):
        self.position = (0, 0)

    def generate(self, width: int, height: int) -> tuple:
        self.position = (random.randint(0, width - 1), random.randint(0, height - 1))
        return self.position