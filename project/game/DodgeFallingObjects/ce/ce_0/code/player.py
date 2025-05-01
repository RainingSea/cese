import pygame

class Player:
    def __init__(self):
        self.position_x = 400
        self.width = 50
        self.height = 50

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.position_x > 0:
            self.position_x -= 5
        if keys[pygame.K_RIGHT] and self.position_x < 750:
            self.position_x += 5

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.position_x, 550, self.width, self.height))