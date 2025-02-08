class Alien:
    def __init__(self, position: tuple):
        self.position = position

    def move(self):
        self.position = (self.position[0], self.position[1] + 1)

    def shoot(self):
        return Projectile(self.position, 'down')