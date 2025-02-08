class Leaderboard:
    def __init__(self):
        self.scores = {}
        self.load_scores()

    def load_scores(self):
        try:
            with open('leaderboard.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(':')
                    self.scores[name] = int(score)
        except FileNotFoundError:
            self.scores = {}

    def save_scores(self):
        with open('leaderboard.txt', 'w') as file:
            for name, score in self.scores.items():
                file.write(f"{name}:{score}\n")

    def update_score(self, name: str, score: int) -> None:
        if name in self.scores:
            if score > self.scores[name]:
                self.scores[name] = score
        else:
            self.scores[name] = score

    def get_high_scores(self) -> list:
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)