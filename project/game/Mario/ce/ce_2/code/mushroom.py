import pygame

class Mushroom:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.position.x, self.position.y, 30, 30)

    def fall(self):
        self.position.y += 5

    def disappear(self):
        self.position.y = -50  # Move off-screen