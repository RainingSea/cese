import pygame

class Obstacle:
    def __init__(self, position: tuple, size: tuple) -> None:
        self.position = pygame.Vector2(position)
        self.size = size

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.position.x, self.position.y, self.size[0], self.size[1]))