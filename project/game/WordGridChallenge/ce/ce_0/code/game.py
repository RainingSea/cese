import pygame
import random

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self) -> float:
        return (pygame.time.get_ticks() - self.start_time) / 1000.0

class Grid:
    def __init__(self):
        self.letters = []
        self.word_list = []

    def generate_grid(self, size: int) -> None:
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def find_words(self) -> list:
        found_words = []
        # Implement word finding logic here
        return found_words

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.word_list = self.load_word_list()

    def load_word_list(self) -> list:
        with open('word_list.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def start_game(self) -> None:
        self.grid.generate_grid(5)  # Example size
        self.timer.start()
        # Implement game loop and event handling here

    def check_word(self, word: str) -> bool:
        return word in self.word_list

    def update_score(self, points: int) -> None:
        self.score.add_points(points)

    def save_score(self, player: str, score: int) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{player}|{score}\n")