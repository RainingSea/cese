import pygame
import random

class Grid:
    def __init__(self):
        self.tiles = []
        self.size = 0

    def create_grid(self, size: int):
        self.size = size
        self.tiles = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]

    def get_tile(self, x: int, y: int) -> int:
        return self.tiles[x][y]

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int):
        self.time_remaining = duration

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self) -> bool:
        return self.time_remaining <= 0

class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points: int):
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.score = Score()

    def start_game(self, difficulty: str):
        size = 4 if difficulty == "easy" else 6 if difficulty == "medium" else 8
        self.grid.create_grid(size)
        self.timer.start_timer(60)  # 60 seconds for the game
        self.score = Score()  # Reset score

    def select_tile(self, x: int, y: int):
        # Handle tile selection logic here
        pass

    def check_path(self) -> bool:
        # Implement path checking logic here
        return True

    def reset_game(self):
        self.score = Score()
        self.timer = Timer()
        self.grid = Grid()