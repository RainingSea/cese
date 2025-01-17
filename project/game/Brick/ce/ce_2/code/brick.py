class Brick:
    def __init__(self, x: int, y: int, lives: int):
        self.x = x
        self.y = y
        self.lives = lives

    def hit(self):
        self.lives -= 1

    def draw(self, screen):
        if self.lives > 0:
            # Draw the brick as a rectangle
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 60, 20))