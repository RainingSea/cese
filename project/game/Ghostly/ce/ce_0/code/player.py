import pygame

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.has_superpower = False
        self.size = 20

    def move(self, direction: str):
        if direction == "up":
            self.y -= 5
        elif direction == "down":
            self.y += 5
        elif direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5

    def eat_pellet(self, pellet):
        if (self.x, self.y) == (pellet.x, pellet.y):
            if pellet.is_superpellet:
                self.has_superpower = True
            pellet.is_superpellet = False  # Pellet is eaten

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.size, self.size))