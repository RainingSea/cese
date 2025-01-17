import pygame

class Player:
    def __init__(self):
        self.position = (0, 0)

    def move(self, direction: str):
        # Implement movement logic
        if direction == 'left':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == 'up':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'down':
            self.position = (self.position[0], self.position[1] + 1)

    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.position[0] * 50 + 25, self.position[1] * 50 + 25), 20)