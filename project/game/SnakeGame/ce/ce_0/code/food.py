import pygame
import random

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.generate_food()

    def generate_food(self):
        self.position = (random.randint(0, 79) * 10, random.randint(0, 59) * 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))