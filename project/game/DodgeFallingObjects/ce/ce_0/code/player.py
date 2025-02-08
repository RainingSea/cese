import pygame

class Player:
    def __init__(self, x_position: int):
        self.x_position = x_position
        self.width = 50
        self.height = 50

    def move(self, direction: str):
        if direction == 'left':
            self.x_position -= 5
        elif direction == 'right':
            self.x_position += 5

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x_position, 550, self.width, self.height))