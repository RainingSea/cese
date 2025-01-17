import pygame

class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.gravity = 1

    def fall(self):
        self.y += self.gravity

    def check_touch(self, mario):
        return (mario.x < self.x + self.width and
                mario.x + mario.width > self.x and
                mario.y < self.y + self.height and
                mario.y + mario.height > self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.width, self.height))