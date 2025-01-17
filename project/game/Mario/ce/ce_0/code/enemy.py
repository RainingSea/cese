import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.direction = random.choice([-1, 1])

    def move_randomly(self):
        self.x += self.direction * 2
        if self.x < 0 or self.x > 750:  # Screen bounds
            self.direction *= -1

    def check_touch(self, mario):
        return (mario.x < self.x + self.width and
                mario.x + mario.width > self.x and
                mario.y < self.y + self.height and
                mario.y + mario.height > self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.width, self.height))