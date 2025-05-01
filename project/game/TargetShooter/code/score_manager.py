import pygame

class ScoreManager:
    def __init__(self):
        self.scores = self.load_scores()

    def calculate_score(self, hit: bool, time_taken: float) -> int:
        if hit:
            return max(0, 100 - int(time_taken * 10))  # Score calculation based on time taken
        return 0

    def save_score(self, player_name: str, score: int) -> None:
        with open('scores.txt', 'a') as f:
            f.write(f"{player_name}|{score}|{pygame.time.get_ticks()}\n")

    def load_scores(self) -> list:
        try:
            with open('scores.txt', 'r') as f:
                return [line.strip().split('|') for line in f.readlines()]
        except FileNotFoundError:
            return []