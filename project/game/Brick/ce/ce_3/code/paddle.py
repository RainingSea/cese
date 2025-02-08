class Paddle:
    def __init__(self, x: int, width: int):
        self.x = x
        self.width = width

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def draw(self, surface):
        import pygame
        pygame.draw.rect(surface, (0, 255, 0), (self.x, 380, self.width, 10))