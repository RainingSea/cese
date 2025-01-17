import os

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        if os.path.exists('leaderboard.txt'):
            with open('leaderboard.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(':')
                    self.scores.append((name, int(score)))

    def save_score(self, name: str, score: int):
        self.scores.append((name, score))
        with open('leaderboard.txt', 'a') as file:
            file.write(f"{name}:{score}\n")

    def get_top_scores(self):
        return sorted(self.scores, key=lambda x: x[1], reverse=True)[:5]