import pygame

class Paddle:
    def __init__(self, x: int, width: int):
        self.x = x
        self.width = width
        self.height = 10

    def move(self, direction: str):
        if direction == "left":
            self.x -= 10
        elif direction == "right":
            self.x += 10

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, 480, self.width, self.height))  # Draw paddle