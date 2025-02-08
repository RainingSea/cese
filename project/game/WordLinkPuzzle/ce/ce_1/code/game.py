import pygame
import time

class Letter:
    def __init__(self, character):
        self.character = character
        self.is_connected = False

    def connect(self):
        self.is_connected = True

    def disconnect(self):
        self.is_connected = False

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration):
        self.time_remaining = duration

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self):
        return self.time_remaining <= 0

class HighScore:
    def __init__(self):
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_high_scores(self):
        return sorted(self.scores, reverse=True)

class Progress:
    def __init__(self):
        self.progress_data = {}

    def save_progress(self, data):
        self.progress_data = data
        with open('progress.txt', 'w') as f:
            for key, value in data.items():
                f.write(f"{key}|{value}\n")

    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    self.progress_data[key] = value
        except FileNotFoundError:
            self.progress_data = {}

class Game:
    def __init__(self):
        self.score = 0
        self.timer = Timer()
        self.difficulty = "Easy"
        self.letters = [Letter(chr(i)) for i in range(65, 91)]  # A-Z

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.timer.start_timer(60)  # 60 seconds for demo
        self.score = 0

    def connect_letters(self, selected_letters):
        word = ''.join(letter.character for letter in selected_letters)
        self.update_score(word)

    def update_score(self, word):
        self.score += len(word)  # Simple scoring based on word length

    def save_progress(self):
        progress = Progress()
        progress.save_progress({'score': self.score, 'difficulty': self.difficulty})

    def load_progress(self):
        progress = Progress()
        progress.load_progress()
        self.score = int(progress.progress_data.get('score', 0))
        self.difficulty = progress.progress_data.get('difficulty', 'Easy')