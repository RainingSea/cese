class Score:
    def __init__(self):
        self.high_score = self.load_score()

    def load_score(self) -> int:
        try:
            with open('score.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0  # Return 0 if file not found or invalid

    def update_score(self, score: int) -> None:
        if score > self.high_score:
            self.high_score = score
            with open('score.txt', 'w') as file:
                file.write(str(self.high_score))