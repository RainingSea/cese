from typing import List, Tuple
import random

class Food:
    def __init__(self):
        self.position: Tuple[int, int] = (0, 0)

    def generate_food(self, snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        while True:
            x = random.randint(0, 19)  # Assuming a 20x20 grid
            y = random.randint(0, 19)
            if (x, y) not in snake_body:
                self.position = (x, y)
                return self.position