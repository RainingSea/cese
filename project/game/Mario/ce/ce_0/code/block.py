import pygame

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def release_mushroom(self):
        return Mushroom(self.x, self.y - 50)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), (self.x, self.y, self.width, self.height))