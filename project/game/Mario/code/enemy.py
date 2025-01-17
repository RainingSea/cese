import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = -1  # Start moving left

    def move_randomly(self):
        self.x += self.direction * 2  # Move left or right by 2 pixels
        if self.x < 0 or self.x > 800:  # Check screen bounds
            self.direction *= -1  # Reverse direction

    def check_collision(self, mario):
        return (self.x < mario.x + 50 and
                self.x + 50 > mario.x and
                self.y < mario.y + 50 and
                self.y + 50 > mario.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, 50, 50))  # Draw Enemy as a blue square