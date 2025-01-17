import pygame

class Ball:
    def __init__(self, x: int, y: int, radius: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 3
        self.dy = -3

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # Add collision detection with walls and paddle here

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius)