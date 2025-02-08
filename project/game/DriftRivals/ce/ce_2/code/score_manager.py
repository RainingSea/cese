from typing import List, Tuple

class ScoreManager:
    def save_score(self, player_name: str, score: float) -> None:
        with open("scores.txt", "a") as f:
            f.write(f"{player_name}|{score}\n")

    def load_scores(self) -> List[Tuple[str, float]]:
        scores = []
        with open("scores.txt", "r") as f:
            for line in f:
                name, score = line.strip().split("|")
                scores.append((name, float(score)))
        return scores