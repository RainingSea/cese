class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.y -= 10  # Simplified jump logic

    def hit_block(self):
        self.score += 10

    def touch_mushroom(self):
        self.score += 50

    def touch_enemy(self):
        self.score -= 20

    def reach_flagpole(self):
        self.score += 100