import pygame
import random
import time

class Grid:
    def __init__(self, size: int):
        self.letters = self.generate_grid(size)

    def generate_grid(self, size: int) -> list:
        return [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def display_grid(self):
        for row in self.letters:
            print(" ".join(row))

    def get_connected_letters(self) -> list:
        # Placeholder for connected letters logic
        return []

class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, length: int):
        self.points += length

    def get_score(self) -> int:
        return self.points

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

class Difficulty:
    def __init__(self):
        self.level = "Easy"

    def set_difficulty(self, level: str):
        self.level = level

    def get_difficulty(self) -> str:
        return self.level

class Game:
    def __init__(self):
        self.grid = Grid(5)
        self.score = Score()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self):
        self.timer.start_timer(60)  # 60 seconds for the game
        print("Game started! Difficulty:", self.difficulty.get_difficulty())
        self.grid.display_grid()

    def connect_letters(self, letters: list) -> bool:
        # Placeholder for connection validation logic
        return True

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write(f"Score: {self.score.get_score()}\n")

    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f:
                score_line = f.readline()
                self.score.points = int(score_line.split(": ")[1])
        except FileNotFoundError:
            print("No progress file found.")