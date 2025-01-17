import json

class ScoreManager:
    def __init__(self):
        self.scores = []

    def load_scores(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            print(f"File {file_path} not found. Initializing empty score list.")
            self.scores = []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}. Initializing empty score list.")
            self.scores = []

    def save_score(self, score: int) -> None:
        self.scores.append(score)
        with open('scores.txt', 'w') as f:
            json.dump(self.scores, f)

    def get_high_scores(self) -> list:
        return sorted(self.scores, reverse=True)[:10]

    def save_to_file(self, score_value: int) -> None:
        with open('scores.txt', 'a') as f:
            f.write(f"{score_value}\n")