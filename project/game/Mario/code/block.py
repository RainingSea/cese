import pygame
from mushroom import Mushroom  # Import Mushroom class

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def release_mushroom(self):
        return Mushroom(self.x + 10, self.y - 20)  # Mushroom above the block

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, self.height))  # Brown block