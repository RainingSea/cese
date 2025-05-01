import pygame

class Basket:
    def __init__(self):
        self.position = [400, 550]
        self.width = 100
        self.speed = 10

    def move_left(self):
        if self.position[0] > 0:
            self.position[0] -= self.speed

    def move_right(self):
        if self.position[0] < 800 - self.width:
            self.position[0] += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.position[0], self.position[1], self.width, 20))