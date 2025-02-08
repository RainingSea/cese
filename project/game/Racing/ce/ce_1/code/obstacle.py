class Obstacle:
    def __init__(self, lane: int, is_hazard: bool):
        self.lane = lane
        self.is_hazard = is_hazard

    def move(self):
        # Logic for moving the obstacle down the lane
        pass