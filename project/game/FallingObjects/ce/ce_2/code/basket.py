import pygame

class Basket:
    def __init__(self, position):
        self.position = position
        self.position_y = 550
        self.width = 100
        self.height = 20

    def move_left(self):
        if self.position > 0:
            self.position -= 5

    def move_right(self):
        if self.position < 800 - self.width:
            self.position += 5

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), (self.position, self.position_y, self.width, self.height))