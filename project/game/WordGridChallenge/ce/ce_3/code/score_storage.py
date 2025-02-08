import json

class ScoreStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.scores = self.load_scores()

    def load_scores(self) -> dict:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_score(self, player: str, score: int) -> None:
        self.scores[player] = score
        with open(self.file_path, 'w') as file:
            json.dump(self.scores, file, indent=4)