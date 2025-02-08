import os
from score_entry import ScoreEntry

class Leaderboard:
    def __init__(self):
        self.scores = []

    def load_scores(self):
        if os.path.exists('scores.txt'):
            with open('scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    self.scores.append(ScoreEntry(name, int(score)))

    def save_score(self, name: str, score: int):
        self.scores.append(ScoreEntry(name, score))
        with open('scores.txt', 'a') as file:
            file.write(f"{name},{score}\n")

    def get_top_scores(self):
        return sorted(self.scores, key=lambda x: x.score, reverse=True)[:5]