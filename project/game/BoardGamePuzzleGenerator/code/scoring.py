import json

class ScoreManager:
    def __init__(self) -> None:
        self.scores = {}
        self.load_scores("scores.json")

    def load_scores(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                self.scores = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading scores: {e}")

    def update_score(self, user: str, score: int) -> None:
        self.scores[user] = self.scores.get(user, 0) + score
        self.save_scores("scores.json")

    def get_scores(self) -> dict:
        return self.scores

    def save_scores(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            json.dump(self.scores, file)