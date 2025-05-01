import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.move_speed = 2
        self.direction = random.choice([-1, 1])  # Randomly choose direction

    def move(self):
        self.x += self.move_speed * self.direction
        if self.x <= 0 or self.x >= 760:  # Reverse direction on hitting screen edges
            self.direction *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))  # Draw Enemy