import pygame

class Player:
    def __init__(self):
        self.vehicle = None
        self.position = pygame.Vector2(400, 300)
        self.speed = 0

    def move(self, direction: str) -> None:
        if direction == "left":
            self.position.x -= 5
        elif direction == "right":
            self.position.x += 5
        elif direction == "up":
            self.position.y -= 5
        elif direction == "down":
            self.position.y += 5

    def update_physics(self) -> None:
        # Implement anti-gravity physics here
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.position.x, self.position.y, 50, 30))