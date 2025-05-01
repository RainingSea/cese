class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, stars_collected: int, time: float, moves: int):
        self.points += stars_collected * 10 - int(time) - moves