import pygame
from mushroom import Mushroom

class Block:
    def __init__(self):
        self.position = pygame.Vector2(100, 400)
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)

    def release_mushroom(self):
        return Mushroom(self.position.x, self.position.y - 50)