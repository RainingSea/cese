import pygame
from typing import List

class WordValidator:
    def __init__(self):
        self.valid_words = []

    def load_words(self, filename: str):
        with open(filename, 'r') as file:
            self.valid_words = [line.strip() for line in file.readlines()]

    def is_valid_word(self, word: str) -> bool:
        return word in self.valid_words

class Game:
    def __init__(self):
        self.letters = []
        self.score = 0
        self.timer = 0
        self.difficulty = ""
        self.word_validator = WordValidator()

    def start_game(self, difficulty: str):
        self.difficulty = difficulty
        self.score = 0
        self.timer = 60  # Starting timer for 60 seconds
        self.word_validator.load_words('words.txt')

    def connect_letters(self, letters: List[str]) -> bool:
        # Logic to connect letters (not implemented)
        return True

    def calculate_score(self, word: str) -> int:
        if self.word_validator.is_valid_word(word):
            self.score += len(word)  # Example scoring logic
            return self.score
        return 0

    def save_progress(self, filename: str):
        with open(filename, 'a') as file:
            file.write(f"player1|{self.score}|{self.timer}|{self.difficulty}\n")

    def load_progress(self, filename: str):
        with open(filename, 'r') as file:
            for line in file:
                print(line.strip())  # For demonstration