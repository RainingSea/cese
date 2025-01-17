class Projectile:
    def __init__(self, position: tuple[int, int], velocity: int):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position = (self.position[0], self.position[1] + self.velocity)