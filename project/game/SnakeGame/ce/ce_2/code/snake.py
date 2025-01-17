from typing import List, Tuple
import random

class Snake:
    def __init__(self):
        self.body: List[Tuple[int, int]] = [(5, 5)]
        self.direction: Tuple[int, int] = (1, 0)  # Initially moving right

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the tail segment

    def grow(self):
        self.body.append(self.body[-1])  # Add a new segment at the tail

    def check_collision(self, wall: bool) -> bool:
        head_x, head_y = self.body[0]
        if wall:
            return head_x < 0 or head_x >= 20 or head_y < 0 or head_y >= 20  # Assuming a 20x20 grid
        return self.check_self_collision()

    def check_self_collision(self) -> bool:
        return self.body[0] in self.body[1:]  # Check if head collides with the body