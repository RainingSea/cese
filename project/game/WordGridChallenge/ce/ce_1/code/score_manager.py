class ScoreManager:
    def __init__(self):
        self.scores = {}

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(':')
                    self.scores[name] = int(score)
        except FileNotFoundError:
            self.scores = {}

    def save_score(self, player: str, score: int):
        self.scores[player] = score
        with open('scores.txt', 'w') as file:
            for name, score in self.scores.items():
                file.write(f"{name}:{score}\n")

    def load_word_list(self):
        try:
            with open('word_list.txt', 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []