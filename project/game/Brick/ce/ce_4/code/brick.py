import pygame

class Brick:
    def __init__(self, life: int):
        self.life = life
        self.color = (255, 0, 0) if life > 0 else (0, 0, 0)  # Red if alive, black if destroyed

    def hit(self):
        self.life -= 1
        self.color = (255, 0, 0) if self.life > 0 else (0, 0, 0)  # Update color based on life

    def is_destroyed(self) -> bool:
        return self.life <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (0, 0, 50, 20))  # Draw brick at (0, 0) for simplicity