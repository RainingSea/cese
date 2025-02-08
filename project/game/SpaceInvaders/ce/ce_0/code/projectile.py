class Projectile:
    def __init__(self, position: tuple, direction: str):
        self.position = position
        self.direction = direction

    def move(self):
        if self.direction == 'up':
            self.position = (self.position[0], self.position[1] - 5)
        elif self.direction == 'down':
            self.position = (self.position[0], self.position[1] + 5)