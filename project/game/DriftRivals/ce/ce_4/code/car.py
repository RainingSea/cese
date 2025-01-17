import pygame

class Car:
    def __init__(self):
        self.position = (400, 300)
        self.speed = 0.0
        self.style_score = 0.0

    def move(self, direction):
        if direction == 'left':
            self.position = (self.position[0] - 5, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 5, self.position[1])

    def drift(self):
        # Simulate drifting and return a style score
        self.style_score = 10.0  # Placeholder for style score calculation
        return self.style_score

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (*self.position, 50, 30))