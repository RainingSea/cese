import pygame

class Wall:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.size = 40

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y, self.size, self.size))