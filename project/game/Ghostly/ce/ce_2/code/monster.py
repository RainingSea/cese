import pygame

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def chase(self, player):
        if player.x > self.x:
            self.x += 1
        elif player.x < self.x:
            self.x -= 1
        if player.y > self.y:
            self.y += 1
        elif player.y < self.y:
            self.y -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 255), (self.x, self.y, 20, 20))