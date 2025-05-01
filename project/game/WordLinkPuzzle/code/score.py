class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, word_length: int):
        self.points += word_length

    def get_score(self) -> int:
        return self.points