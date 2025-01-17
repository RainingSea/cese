class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int):
        self.points += points

    def get_score(self) -> int:
        return self.points