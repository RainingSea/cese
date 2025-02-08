import os

class HighScores:
    def __init__(self):
        self.scores = []

    def load_scores(self) -> None:
        if os.path.exists('high_scores.txt'):
            with open('high_scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split('|')
                    self.scores.append((name, int(score)))

    def save_score(self, name: str, score: int) -> None:
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        with open('high_scores.txt', 'w') as file:
            for name, score in self.scores:
                file.write(f"{name}|{score}\n")