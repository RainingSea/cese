import pygame

class Brick:
    def __init__(self, x: int, y: int, lives: int):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 20
        self.lives = lives

    def hit(self):
        self.lives -= 1

    def draw(self, surface):
        if self.lives > 0:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))