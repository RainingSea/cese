import random

class Object:
    def __init__(self, x: int, y: int, speed: int):
        self.x_position = x
        self.y_position = y
        self.fall_speed = speed

    def fall(self):
        self.y_position += self.fall_speed

    def draw(self, surface):
        # For demonstration, we will represent the object as a rectangle
        pygame.draw.rect(surface, (255, 0, 0), (self.x_position, self.y_position, 20, 20))