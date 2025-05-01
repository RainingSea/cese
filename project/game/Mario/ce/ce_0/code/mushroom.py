import pygame

class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.fall_speed = 2

    def fall(self):
        self.y += self.fall_speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Draw Mushroom