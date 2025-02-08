import pygame
import random

class Score:
    def __init__(self):
        self.current_score = 0

    def add_score(self, points: int) -> None:
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int) -> None:
        self.time_remaining = duration

    def update_timer(self) -> int:
        if self.time_remaining > 0:
            self.time_remaining -= 1
        return self.time_remaining

class Grid:
    def __init__(self):
        self.letters = []
        self.word_list = []

    def generate_grid(self, size: int) -> None:
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]
        self.load_word_list()

    def display_grid(self) -> None:
        for row in self.letters:
            print(" ".join(row))

    def get_selected_letters(self) -> str:
        # This is a placeholder for the actual selection logic
        return "".join(random.choice(random.choice(self.letters)))

    def load_word_list(self) -> None:
        try:
            with open('word_list.txt', 'r') as file:
                self.word_list = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("Word list file not found!")

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()

    def start_game(self, level: int) -> None:
        size = 4 + level  # Example: level 0 -> 4x4, level 1 -> 5x5, etc.
        self.grid.generate_grid(size)
        self.timer.start_timer(60)  # Start with 60 seconds
        self.score.add_score(0)  # Reset score

    def update_score(self, points: int) -> None:
        self.score.add_score(points)

    def check_word(self, word: str) -> bool:
        return word in self.grid.word_list

    def reset_game(self) -> None:
        self.start_game(0)  # Reset to level 0