import pygame
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.word_list = WordList()
        self.word_list.load_words('word_list.txt')

    def start_game(self):
        self.grid.generate_grid(size=4)  # Example size
        self.timer.start()
        self.display_grid()

    def check_word(self, word):
        return self.word_list.is_valid_word(word)

    def update_score(self, word):
        self.score.add_points(len(word))

    def display_grid(self):
        # Placeholder for grid display logic
        pass

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size):
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def get_letter(self, x, y):
        return self.letters[x][y]

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def get_score(self):
        return self.points

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        return (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds

class WordList:
    def __init__(self):
        self.words = []

    def load_words(self, file_path):
        with open(file_path, 'r') as file:
            self.words = [line.strip() for line in file.readlines()]

    def is_valid_word(self, word):
        return word in self.words