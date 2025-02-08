import pygame
import random

class LetterGrid:
    def __init__(self, size=(5, 5)):
        self.size = size
        self.letters = self.generate_letters()

    def generate_letters(self):
        return [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(self.size[1])] for _ in range(self.size[0])]

    def display_grid(self):
        for row in self.letters:
            print(' '.join(row))

    def connect_letters(self, start: tuple, end: tuple) -> str:
        # Assuming start and end are (row, col) tuples
        word = ''
        if start[0] == end[0]:  # Horizontal
            for col in range(start[1], end[1] + 1):
                word += self.letters[start[0]][col]
        elif start[1] == end[1]:  # Vertical
            for row in range(start[0], end[0] + 1):
                word += self.letters[row][start[1]]
        return word

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, length: int):
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
        self.level = 'Easy'

    def set_difficulty(self, level: str):
        self.level = level

    def get_difficulty(self) -> str:
        return self.level

class Game:
    def __init__(self):
        self.letter_grid = LetterGrid()
        self.score = Score()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self):
        self.timer.start_timer(60)  # Start with 60 seconds

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write(f'Score:{self.score.get_score()}\n')
            f.write(f'Time Remaining:{self.timer.time_remaining}\n')

    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f:
                lines = f.readlines()
                self.score.points = int(lines[0].split(':')[1])
                self.timer.time_remaining = int(lines[1].split(':')[1])
        except FileNotFoundError:
            print("No progress file found.")

    def update_score(self, word: str):
        self.score.add_points(len(word))