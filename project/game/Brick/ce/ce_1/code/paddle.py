import pygame

class Paddle:
    def __init__(self, x: int, width: int, height: int):
        self.x = x
        self.width = width
        self.height = height

    def move(self, direction: str):
        if direction == 'left' and self.x > 0:
            self.x -= 5
        elif direction == 'right' and self.x < 800 - self.width:
            self.x += 5

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, 580, self.width, self.height))