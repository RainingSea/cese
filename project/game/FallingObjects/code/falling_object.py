import pygame
import random

class Object:
    def __init__(self):
        self.position = [random.randint(0, 780), 0]
        self.speed = random.randint(3, 7)

    def fall(self):
        self.position[1] += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.position[0] + 10, self.position[1] + 10), 10)

    def reset_position(self):
        self.position[1] = 0
        self.position[0] = random.randint(0, 780)