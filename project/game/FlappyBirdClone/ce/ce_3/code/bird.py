import pygame

class Bird:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 34
        self.height = 24
        self.gravity = 1
        self.flap_strength = -15

    def flap(self) -> None:
        self.y += self.flap_strength

    def fall(self) -> None:
        self.y += self.gravity

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)