class ScoreManager:
    def __init__(self):
        self.scores = []

    def load_scores(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            for line in file:
                player_name, score = line.strip().split('|')
                self.scores.append((player_name, int(score)))

    def save_score(self, player_name: str, score: int) -> None:
        self.scores.append((player_name, score))
        with open("scores.txt", 'a') as file:
            file.write(f"{player_name}|{score}\n")