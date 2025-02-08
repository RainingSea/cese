from projectile import Projectile

class Alien:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self):
        self.x += 1  # Simple horizontal movement

    def shoot(self) -> Projectile:
        return Projectile(self.x, self.y, speed=5)