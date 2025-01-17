import pygame
from projectile import Projectile

class Alien:
    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.width = 50
        self.height = 30
        self.color = (255, 0, 0)  # Red color

    def move(self):
        self.position = (self.position[0], self.position[1] + 1)

    def shoot(self):
        return Projectile((self.position[0] + self.width // 2, self.position[1] + self.height), 10)