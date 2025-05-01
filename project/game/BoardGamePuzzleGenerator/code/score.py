class Score:
    def __init__(self):
        self.user_score = 0
        self.load_scores()

    def calculate_score(self, time: float, accuracy: bool) -> int:
        base_score = 1000
        time_penalty = time * 10
        if accuracy:
            return max(base_score - time_penalty, 0)
        return 0

    def update_score(self, user: str, score: int) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{user}|{score}\n")

    def load_scores(self) -> None:
        self.scores = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    user, score = line.strip().split('|')
                    self.scores[user] = int(score)
        except FileNotFoundError:
            pass