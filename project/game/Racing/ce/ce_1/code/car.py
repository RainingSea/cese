class Car:
    def __init__(self):
        self.speed = 0
        self.lane = 1  # Start in the middle lane

    def move_up(self):
        if self.lane > 0:
            self.lane -= 1

    def move_down(self):
        if self.lane < 2:
            self.lane += 1

    def stop(self):
        self.speed = 0