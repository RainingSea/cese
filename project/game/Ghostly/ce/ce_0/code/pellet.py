import pygame

class Pellet:
    def __init__(self, x: int, y: int, is_superpellet: bool):
        self.x = x
        self.y = y
        self.is_superpellet = is_superpellet
        self.size = 10

    def draw(self, screen):
        color = (255, 255, 0) if self.is_superpellet else (255, 255, 255)
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)