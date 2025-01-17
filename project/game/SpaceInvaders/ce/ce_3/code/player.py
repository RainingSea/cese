from projectile import Projectile

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, direction: str):
        if direction == 'left':
            self.x -= 5
        elif direction == 'right':
            self.x += 5

    def shoot(self) -> Projectile:
        return Projectile(self.x, self.y, speed=10)