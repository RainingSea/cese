import pygame

class Enemy:
    def __init__(self):
        self.position = pygame.Vector2(300, 500)
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)
        self.direction = 1  # 1 for right, -1 for left

    def move(self):
        self.position.x += self.direction * 2
        if self.position.x > 750 or self.position.x < 0:
            self.direction *= -1
        self.rect.topleft = (self.position.x, self.position.y)