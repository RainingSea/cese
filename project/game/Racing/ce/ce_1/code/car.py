class Car:
    def __init__(self, lane: int):
        self.lane = lane
        self.speed = 0

    def move_up(self):
        if self.lane > 0:
            self.lane -= 1

    def move_down(self):
        if self.lane < 2:
            self.lane += 1

    def shift_left(self):
        self.speed = max(0, self.speed - 1)

    def shift_right(self):
        self.speed += 1

    def stop(self):
        self.speed = 0