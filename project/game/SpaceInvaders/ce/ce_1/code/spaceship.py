import pygame

class Spaceship:
    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.width = 50
        self.height = 30
        self.color = (0, 255, 0)  # Green color

    def move_left(self):
        self.position = (self.position[0] - 5, self.position[1])

    def move_right(self):
        self.position = (self.position[0] + 5, self.position[1])

    def shoot(self):
        return Projectile((self.position[0] + self.width // 2, self.position[1]), -10)