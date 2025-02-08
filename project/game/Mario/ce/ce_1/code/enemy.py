class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x -= 2  # Simplified enemy movement logic

    def check_collision(self, mario):
        if (mario.x < self.x + 20 and
            mario.x + 20 > self.x and
            mario.y < self.y + 20 and
            mario.y + 20 > self.y):
            mario.touch_enemy()
            return True
        return False