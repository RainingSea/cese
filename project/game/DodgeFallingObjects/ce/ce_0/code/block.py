import pygame

class Block:
    def __init__(self, x_position: int, speed: int):
        self.x_position = x_position
        self.y_position = 0
        self.speed = speed

    def fall(self):
        self.y_position += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x_position, self.y_position, 50, 50))