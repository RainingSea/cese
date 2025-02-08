import pygame

class Ball:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dx = 5
        self.dy = -5
        self.radius = 10

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius)  # Draw ball