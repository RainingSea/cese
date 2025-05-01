import pygame
import os

class Game:
    def __init__(self):
        self.score = 0
        self.timer = 60  # default timer set to 60 seconds
        self.difficulty = 'easy'
        self.word_manager = WordManager()
        self.score_manager = ScoreManager()

    def start_game(self):
        # Initialize Pygame and start the game loop
        pygame.init()
        self.load_progress()
        # Game loop logic would go here

    def update_score(self, points: int):
        self.score += points

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write(f'score|{self.score}\n')
            f.write(f'timer|{self.timer}\n')
            f.write(f'difficulty|{self.difficulty}\n')

    def load_progress(self):
        if os.path.exists('progress.txt'):
            with open('progress.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    if key == 'score':
                        self.score = int(value)
                    elif key == 'timer':
                        self.timer = int(value)
                    elif key == 'difficulty':
                        self.difficulty = value

class WordManager:
    def __init__(self):
        self.letters = ['a', 'b', 'c', 'd', 'e']  # Example letters

    def form_word(self, selected_letters: list) -> str:
        return ''.join(selected_letters)

    def validate_word(self, word: str) -> bool:
        # Simple validation for demo purposes
        return word in ['abc', 'de', 'abcd', 'abcde']  # Example valid words

class ScoreManager:
    def __init__(self):
        self.high_scores = []

    def add_score(self, score: int):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 10:
            self.high_scores.pop()  # Keep only top 10 scores

    def get_high_scores(self) -> list:
        return self.high_scores