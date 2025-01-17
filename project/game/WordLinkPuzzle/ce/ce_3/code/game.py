import pygame
import random

class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, word_length: int) -> None:
        self.points += word_length

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self):
        self.time_left = 0

    def start_timer(self, duration: int) -> None:
        self.time_left = duration

    def update_timer(self) -> int:
        if self.time_left > 0:
            self.time_left -= 1
        return self.time_left

class Difficulty:
    def __init__(self):
        self.level = "Easy"

    def set_difficulty(self, level: str) -> None:
        self.level = level

    def get_difficulty(self) -> str:
        return self.level

class Grid:
    def __init__(self):
        self.letters = self.generate_grid()

    def generate_grid(self) -> list:
        return [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)] for _ in range(5)]

    def display_grid(self) -> None:
        for row in self.letters:
            print(" ".join(row))

    def connect_letters(self, start: tuple, end: tuple) -> str:
        # Placeholder for actual connection logic
        return "Connected letters from {} to {}".format(start, end)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self) -> None:
        self.timer.start_timer(60)  # Start with a 60 seconds timer
        self.grid.display_grid()

    def save_progress(self) -> None:
        with open('progress.txt', 'w') as file:
            file.write(f"Score: {self.score.get_score()}\n")
            file.write(f"Time Left: {self.timer.time_left}\n")

    def load_progress(self) -> None:
        try:
            with open('progress.txt', 'r') as file:
                lines = file.readlines()
                self.score.points = int(lines[0].split(": ")[1])
                self.timer.time_left = int(lines[1].split(": ")[1])
        except FileNotFoundError:
            print("No progress found. Starting a new game.")