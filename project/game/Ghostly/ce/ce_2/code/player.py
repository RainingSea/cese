import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_superpower = False

    def move(self, direction: str):
        if direction == 'left':
            self.x -= 5
        elif direction == 'right':
            self.x += 5
        elif direction == 'up':
            self.y -= 5
        elif direction == 'down':
            self.y += 5

    def eat_pellet(self):
        # Logic to eat pellet
        pass

    def eat_superpellet(self):
        self.has_superpower = True