import pygame

class Monster:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.size = 20

    def chase(self, player):
        if player.x > self.x:
            self.x += 2
        elif player.x < self.x:
            self.x -= 2
        if player.y > self.y:
            self.y += 2
        elif player.y < self.y:
            self.y -= 2

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))