import pygame
import random

class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.fall_speed = 1  # Define fall speed

    def fall(self):
        self.y += self.fall_speed  # Mushroom falls every update
        if self.y > 600:  # Reset mushroom if it falls off the screen
            self.y = 0
            self.x = random.randint(0, 770)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))