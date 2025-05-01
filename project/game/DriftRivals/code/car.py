import pygame

class Car:
    def __init__(self):
        self.position = pygame.Vector2(400, 300)
        self.speed = 0
        self.drift_metrics = {}

    def move(self, direction: str) -> None:
        if self.speed > 0:  # Only move if speed is greater than zero
            if direction == "left":
                self.position.x -= 5
            elif direction == "right":
                self.position.x += 5
            elif direction == "forward":
                self.position.y -= 5
            elif direction == "backward":
                self.position.y += 5

    def drift(self) -> None:
        self.drift_metrics['style'] = 'perfect'
        self.drift_metrics['angle'] = 30  # Example value

    def update_position(self) -> None:
        # Update car position based on speed and other factors
        pass

    def render(self, screen) -> None:
        pygame.draw.rect(screen, (255, 0, 0), (self.position.x, self.position.y, 50, 30))