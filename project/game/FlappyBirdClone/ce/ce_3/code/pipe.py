import pygame
import random

class Pipe:
    def __init__(self, x: int, height: int, gap: int):
        self.x = x
        self.height = height
        self.gap = gap
        self.width = 52

    def move(self) -> None:
        self.x -= 5

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, 0, self.width, self.height), pygame.Rect(self.x, self.height + self.gap, self.width, 600 - (self.height + self.gap))