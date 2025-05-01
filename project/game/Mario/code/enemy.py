import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.direction = random.choice([-1, 1])  # Randomly set direction
        self.move_speed = 2  # Define move speed

    def move(self):
        self.x += self.move_speed * self.direction  # Move left or right
        if self.x <= 0 or self.x >= 760:  # Check screen edges
            self.direction *= -1  # Reverse direction on hitting screen edges

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))