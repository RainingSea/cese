import pygame

class FallingObject:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.speed = 5

    def fall(self):
        self.position_y += self.speed

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (self.position_x, self.position_y), 10)