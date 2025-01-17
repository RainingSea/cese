import json

class UserProgress:
    def __init__(self, filename='progress.txt'):
        self.filename = filename
        self.progress_data = {}

    def save(self, data: dict) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load(self) -> dict:
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}