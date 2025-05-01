import json

class Score:
    def __init__(self):
        self.player_scores = self.load_scores()

    def save_score(self, name: str, score: int):
        self.player_scores[name] = score
        with open('scores.txt', 'w') as f:
            for player, score in self.player_scores.items():
                f.write(f"{player}|{score}\n")

    def load_scores(self) -> dict:
        scores = {}
        try:
            with open('scores.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split('|')
                    scores[name] = int(score)
        except FileNotFoundError:
            pass  # File does not exist yet
        return scores