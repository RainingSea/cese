import pygame

class Star:
    def __init__(self, position: tuple):
        self.position = position
        self.collected = False

    def is_collected(self) -> bool:
        return self.collected

    def render(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 255, 0), (self.position[0] * 20 + 10, self.position[1] * 20 + 10), 10)  # Draw star