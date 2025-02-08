class Spaceship:
    def __init__(self, position: tuple):
        self.position = position

    def move(self, direction: str):
        if direction == 'left':
            self.position = (self.position[0] - 5, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 5, self.position[1])

    def shoot(self):
        return Projectile((self.position[0], self.position[1] - 10), 'up')