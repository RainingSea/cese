class Leaderboard:
    def __init__(self):
        self.scores = []

    def update_leaderboard(self, player_name: str, new_score: int) -> None:
        self.scores.append((player_name, new_score))
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)[:10]  # Keep top 10 scores

    def get_top_scores(self) -> list:
        return self.scores