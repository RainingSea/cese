import pygame

class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 1  # Gravity effect

    def fall(self):
        self.y += self.gravity  # Mushroom falls down

    def check_collision(self, mario):
        return (self.x < mario.x + 50 and
                self.x + 50 > mario.x and
                self.y < mario.y + 50 and
                self.y + 50 > mario.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 30, 30))  # Draw Mushroom as a green square