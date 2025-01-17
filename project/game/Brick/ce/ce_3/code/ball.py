class Ball:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dx = 3
        self.dy = -3

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        import pygame
        pygame.draw.circle(surface, (0, 0, 255), (self.x, self.y), 10)