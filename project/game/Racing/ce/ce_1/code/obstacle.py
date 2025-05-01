class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.y = 0
        self.slows_down = False

    def move(self):
        self.y += 5  # Move down the screen