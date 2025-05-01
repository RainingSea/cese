class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points: int):
        self.current_score += points

    def get_score(self):
        return self.current_score