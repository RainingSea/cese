import pygame
import random

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, 59) * 10
        y = random.randint(0, 39) * 10
        self.position = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))