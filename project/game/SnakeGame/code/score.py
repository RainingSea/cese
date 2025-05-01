class Score:
    def __init__(self):
        self.current_score = 0

    def increase(self):
        self.current_score += 1

    def get_score(self):
        return self.current_score