class Score:
    def __init__(self):
        self.current_score = 0

    def calculate_score(self, drift_metrics) -> None:
        if drift_metrics.get('style') == 'perfect':
            self.current_score += 100

    def save_score(self, player_name: str) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name},{self.current_score}\n")

    def load_scores(self) -> dict:
        scores = {}
        try:
            with open('scores.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split(',')
                    scores[name] = int(score)
        except FileNotFoundError:
            pass  # File doesn't exist yet
        return scores