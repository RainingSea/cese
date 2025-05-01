import pygame

class Player:
    def __init__(self):
        self.position = (1, 1)

    def move(self, direction: str):
        if direction == "up":
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == "left":
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + 1, self.position[1])

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] * 40, self.position[1] * 40, 40, 40))