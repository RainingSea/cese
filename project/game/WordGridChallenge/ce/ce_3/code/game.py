import random
import time

class Game:
    def __init__(self):
        self.grid = []
        self.score = 0
        self.timer = 60  # 60 seconds
        self.words_found = []

    def start_game(self):
        self.generate_grid(level=1)
        self.update_timer()

    def generate_grid(self, level: int) -> None:
        size = 5 + level  # Increase grid size with level
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(size):
            for j in range(size):
                self.grid[i][j] = random.choice(letters)

    def check_word(self, word: str) -> bool:
        if word in self.words_found:
            return False
        # Simulate word checking logic (to be implemented)
        self.words_found.append(word)
        return True

    def update_score(self, points: int) -> None:
        self.score += points

    def update_timer(self) -> None:
        while self.timer > 0:
            time.sleep(1)
            self.timer -= 1