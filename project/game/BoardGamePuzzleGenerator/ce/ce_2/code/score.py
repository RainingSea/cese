class ScoreManager:
    def __init__(self):
        self.score = 0

    def calculate_score(self, time_taken: float, accuracy: bool) -> int:
        if accuracy:
            self.score += max(100 - int(time_taken), 0)  # Simple scoring logic
        else:
            self.score -= 10  # Penalty for incorrect answer
        return self.score

    def get_score(self) -> int:
        return self.score