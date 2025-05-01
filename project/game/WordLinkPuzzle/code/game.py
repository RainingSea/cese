import pygame
import random
import os
from timer import Timer
from score import Score
from difficulty import Difficulty
from word_manager import WordManager
from grid import Grid

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.word_manager = WordManager()
        self.difficulty = Difficulty()
        self.load_words("words.txt")
        self.load_progress("username")  # Load progress for a specific user

    def start_game(self):
        self.timer.start_timer(60)  # 60 seconds for the game
        while not self.timer.is_time_up():
            self.grid.display()
            self.timer.update_timer()  # Update timer each loop
            self.handle_user_input()  # Handle user input and game logic here
            pygame.display.flip()
        self.save_progress("username")  # Save progress for a specific user

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Placeholder for letter selection logic
                selected_letter = self.get_selected_letter(event.key)
                if selected_letter:
                    self.grid.connect_letters(selected_letter)

    def get_selected_letter(self, key):
        # Map key presses to grid letters (this is a placeholder)
        # Example: return a list of letters based on key pressed
        return []

    def save_progress(self, username: str):
        os.makedirs('progress', exist_ok=True)  # Ensure progress directory exists
        with open(f'progress/{username}.txt', 'w') as f:
            f.write(f'Score: {self.score.get_score()}\n')
            f.write(f'Timer: {self.timer.time_left}\n')
            f.write(f'Difficulty: {self.difficulty.get_difficulty()}\n')

    def load_progress(self, username: str):
        try:
            with open(f'progress/{username}.txt', 'r') as f:
                data = f.readlines()
                self.score.points = int(data[0].split(': ')[1])
                self.timer.time_left = int(data[1].split(': ')[1])
                self.difficulty.set_difficulty(int(data[2].split(': ')[1]))
        except FileNotFoundError:
            print("No saved progress found.")

    def load_words(self, file_path: str):
        self.word_manager.load_words(file_path)