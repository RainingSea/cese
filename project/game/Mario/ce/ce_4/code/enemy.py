import random

class Enemy:
    def __init__(self, position: tuple):
        self.position = position

    def move(self) -> None:
        # Randomly move the enemy left or right
        direction = random.choice([-1, 1])
        self.position = (self.position[0] + direction, self.position[1])

    def check_collision(self, mario: 'Mario') -> bool:
        # Simple collision detection
        return self.position == mario.position