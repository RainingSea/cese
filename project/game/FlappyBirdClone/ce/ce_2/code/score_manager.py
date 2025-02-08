import os

class ScoreManager:
    def __init__(self):
        self.high_scores = []
        self.load_high_scores()

    def load_high_scores(self):
        if os.path.exists('high_scores.txt'):
            with open('high_scores.txt', 'r') as file:
                self.high_scores = [int(line.strip()) for line in file.readlines()]

    def save_high_score(self, score: int):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep top 5 scores
        with open('high_scores.txt', 'w') as file:
            for high_score in self.high_scores:
                file.write(f"{high_score}\n")

    def get_high_scores(self) -> list:
        return self.high_scores