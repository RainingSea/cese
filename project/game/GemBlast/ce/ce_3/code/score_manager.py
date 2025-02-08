import os

class ScoreManager:
    def save_score(self, player_name: str, score: int):
        with open('scores.txt', 'a') as f:
            f.write(f"{player_name}|{score}\n")

    def load_scores(self) -> List[Tuple[str, int]]:
        scores = []
        if os.path.exists('scores.txt'):
            with open('scores.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split('|')
                    scores.append((name, int(score)))
        return scores