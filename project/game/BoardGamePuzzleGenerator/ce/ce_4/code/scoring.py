class Scoring:
    def __init__(self):
        self.score = 0

    def calculate_score(self, time_taken: float, is_correct: bool) -> int:
        if is_correct:
            self.score = max(0, 100 - int(time_taken))  # Simple scoring logic
        else:
            self.score = 0
        return self.score

    def get_score(self) -> int:
        return self.score