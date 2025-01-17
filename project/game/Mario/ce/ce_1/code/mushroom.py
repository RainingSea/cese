class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fall(self):
        self.y += 5  # Simplified falling logic

    def check_collision(self, mario):
        if (mario.x < self.x + 20 and
            mario.x + 20 > self.x and
            mario.y < self.y + 20 and
            mario.y + 20 > self.y):
            mario.touch_mushroom()
            return True
        return False