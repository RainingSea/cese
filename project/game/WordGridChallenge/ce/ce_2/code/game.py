import random
import time

class Game:
    def __init__(self):
        self.grid = []
        self.word_list = []
        self.score = 0
        self.timer = 0

    def generate_grid(self, size: int) -> list:
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.grid = [[random.choice(letters) for _ in range(size)] for _ in range(size)]
        return self.grid

    def load_words(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            self.word_list = [line.strip() for line in file.readlines()]
        return self.word_list

    def start_timer(self) -> None:
        self.timer = time.time()

    def check_word(self, word: str) -> bool:
        return word in self.word_list

    def update_score(self, points: int) -> None:
        self.score += points

    def save_score(self, player_name: str) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name}|{self.score}\n")