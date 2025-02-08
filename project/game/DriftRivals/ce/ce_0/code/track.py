import pygame

class Track:
    def __init__(self, name: str, path: list):
        self.name = name
        self.path = path

    def draw(self, surface):
        if len(self.path) > 1:
            pygame.draw.lines(surface, (255, 0, 0), False, self.path, 2)