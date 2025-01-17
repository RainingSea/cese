import random
import time

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start(self) -> None:
        self.start_time = time.time()

    def get_time_elapsed(self) -> float:
        return time.time() - self.start_time

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int) -> None:
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def get_adjacent_letters(self, x: int, y: int) -> list:
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.letters) and 0 <= ny < len(self.letters[0]):
                    adjacent.append(self.letters[nx][ny])
        return adjacent

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()

    def start_game(self) -> None:
        self.timer.start()
        self.grid.generate_grid(size=4)  # Example grid size

    def update_score(self, word: str) -> None:
        self.score.add_points(len(word))  # Example scoring based on word length

    def display_grid(self) -> None:
        for row in self.grid.letters:
            print(' '.join(row))

    def check_word_selection(self, selected_letters: list) -> bool:
        # Placeholder for actual word checking logic
        return True