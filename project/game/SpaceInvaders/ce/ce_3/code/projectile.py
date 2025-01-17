class Projectile:
    def __init__(self, x: int, y: int, speed: int):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.y -= self.speed