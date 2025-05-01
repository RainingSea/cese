import pygame

class Block:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.width = 50
        self.height = 50
        self.speed = 5

    def fall(self):
        self.position_y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.position_x, self.position_y, self.width, self.height))