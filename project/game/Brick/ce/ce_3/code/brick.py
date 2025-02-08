class Brick:
    def __init__(self, x: int, y: int, lives: int):
        self.lives = lives
        self.x = x
        self.y = y

    def hit(self):
        self.lives -= 1

    def draw(self, surface):
        if self.lives > 0:
            # Drawing a simple rectangle for the brick
            import pygame
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 50, 20))