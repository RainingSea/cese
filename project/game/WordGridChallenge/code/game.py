import pygame
import random
from typing import List, Dict

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score_manager = ScoreManager()
        self.timer = Timer()
        self.word_list = WordList()
        self.word_list.load_words('word_list.txt')
        self.load_game_state('game_state.txt')

    def start_game(self):
        self.grid.generate_grid(4)  # Example size
        self.timer.start()
        self.play_game()

    def play_game(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Additional game logic would go here

    def check_word(self, word: str) -> bool:
        return self.word_list.is_valid_word(word) and self.grid.contains_word(word)

    def update_score(self, points: int):
        self.score_manager.add_points(points)

    def save_score(self, player: str, score: int):
        self.score_manager.save_score(player, score)

    def save_game_state(self, file_path: str):
        with open(file_path, 'w') as file:
            file.write(f"current_grid: {self.grid.letters}\n")
            file.write(f"current_time: {self.timer.get_elapsed_time()}\n")

    def load_game_state(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split(': ')
                    if key == 'current_grid':
                        self.grid.letters = eval(value)  # Caution: eval can be dangerous
                    elif key == 'current_time':
                        self.timer.start_time = float(value)
        except FileNotFoundError:
            pass

class Grid:
    def __init__(self):
        self.letters: List[List[str]] = []

    def generate_grid(self, size: int):
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def find_words(self) -> List[str]:
        found_words = []
        for row in self.letters:
            found_words.extend(self.find_words_in_line(row))
        for col in zip(*self.letters):
            found_words.extend(self.find_words_in_line(col))
        found_words.extend(self.find_words_in_diagonals())
        return found_words

    def find_words_in_line(self, line: List[str]) -> List[str]:
        line_str = ''.join(line)
        return [word for word in line_str.split() if word in self.word_list.words]

    def find_words_in_diagonals(self) -> List[str]:
        diagonals = []
        size = len(self.letters)
        for i in range(size):
            diagonals.append(''.join(self.letters[j][j + i] for j in range(size - i)))  # Down-right
            diagonals.append(''.join(self.letters[j][i - j] for j in range(i + 1)))  # Up-right
        return [word for diag in diagonals for word in self.find_words_in_line(diag)]

    def contains_word(self, word: str) -> bool:
        return word in self.find_words()

class ScoreManager:
    def __init__(self):
        self.score = Score()
        self.load_scores()

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    username, score = line.strip().split(':')
                    self.score.scores[username] = int(score)
        except FileNotFoundError:
            pass

    def save_score(self, username: str, score: int):
        self.score.scores[username] = score
        with open('scores.txt', 'a') as file:
            file.write(f"{username}:{score}\n")

class Score:
    def __init__(self):
        self.scores: Dict[str, int] = {}

    def add_points(self, points: int):
        default_player = 'default_player'
        if default_player not in self.scores:
            self.scores[default_player] = 0
        self.scores[default_player] += points

    def get_score(self) -> int:
        default_player = 'default_player'
        return self.scores.get(default_player, 0)

class Timer:
    def __init__(self):
        self.start_time: float = 0.0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self) -> float:
        return (pygame.time.get_ticks() - self.start_time) / 1000.0

class WordList:
    def __init__(self):
        self.words: List[str] = []

    def load_words(self, file_path: str):
        with open(file_path, 'r') as file:
            self.words = [line.strip() for line in file]

    def is_valid_word(self, word: str) -> bool:
        return word in self.words