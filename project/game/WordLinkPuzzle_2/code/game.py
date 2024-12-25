import pygame
import random
from typing import List

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int) -> None:
        """Generates a random letter grid of given size."""
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def get_letters(self) -> List[List[str]]:
        """Returns the current letter grid."""
        return self.letters

class Score:
    def __init__(self):
        self.total_score = 0

    def update_score(self, word: str) -> None:
        """Updates the score based on the length of the formed word and complexity."""
        base_score = len(word)  # Base score based on word length
        bonus_score = self.calculate_bonus(word)  # Calculate bonus for complexity
        self.total_score += base_score + bonus_score  # Update total score

    def calculate_bonus(self, word: str) -> int:
        """Calculates bonus points for rare or complex words."""
        # Example: Bonus points for words longer than 5 letters
        if len(word) > 5:
            return 5  # Bonus for longer words
        return 0  # No bonus for shorter words

    def get_score(self) -> int:
        """Returns the current score."""
        return self.total_score

class Timer:
    def __init__(self):
        self.time_remaining = 0
        self.is_paused = False
        self.paused_time = 0

    def start_timer(self, duration: int) -> None:
        """Starts the timer with a given duration."""
        self.time_remaining = duration
        self.is_paused = False

    def pause_timer(self) -> None:
        """Pauses the timer."""
        if not self.is_paused:
            self.paused_time = self.time_remaining
            self.is_paused = True

    def resume_timer(self) -> None:
        """Resumes the timer."""
        if self.is_paused:
            self.time_remaining = self.paused_time
            self.is_paused = False

    def check_time(self) -> int:
        """Returns the remaining time."""
        return self.time_remaining

    def decrement_time(self) -> None:
        """Decreases the remaining time by 1 second."""
        if not self.is_paused and self.time_remaining > 0:
            self.time_remaining -= 1

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.formed_words = []
        self.load_dictionary()
        self.load_sounds()

    def load_dictionary(self) -> None:
        """Loads valid words from the dictionary file."""
        with open('dictionary.txt', 'r') as file:
            self.valid_words = set(file.read().strip().split('|'))  # Adjusted to use '|' as delimiter

    def load_sounds(self) -> None:
        """Loads sound effects for the game."""
        self.word_formed_sound = pygame.mixer.Sound('sounds/word_formed.wav')
        self.bonus_points_sound = pygame.mixer.Sound('sounds/bonus_points.wav')
        self.timer_warning_sound = pygame.mixer.Sound('sounds/timer_warning.wav')

    def start_game(self) -> None:
        """Starts the game by generating the grid and starting the timer."""
        self.grid.generate_grid(4)  # Example grid size
        self.timer.start_timer(60)  # 60 seconds timer
        self.main_game_loop()

    def main_game_loop(self) -> None:
        """Main loop for the game logic (event handling, updating display, etc.)."""
        while self.timer.check_time() > 0:
            self.timer.decrement_time()
            # Placeholder for the main game loop logic
            # Here you would handle user input and word formation logic
            pass

    def pause_game(self) -> None:
        """Pauses the game timer."""
        self.timer.pause_timer()

    def save_progress(self) -> None:
        """Saves the current game progress to a file."""
        with open('game_progress.txt', 'w') as file:
            file.write(f"{self.grid.get_letters()}\n{self.score.get_score()}\n{self.timer.check_time()}\n{self.formed_words}")

    def load_progress(self) -> None:
        """Loads the game progress from a file."""
        with open('game_progress.txt', 'r') as file:
            data = file.readlines()
            self.grid.letters = eval(data[0].strip())
            self.score.total_score = int(data[1].strip())
            self.timer.time_remaining = int(data[2].strip())
            self.formed_words = eval(data[3].strip())

    def validate_word(self, word: str) -> bool:
        """Validates if the formed word is in the dictionary."""
        return word in self.valid_words

    def play_word_formed_sound(self) -> None:
        """Plays sound when a word is formed successfully."""
        self.word_formed_sound.play()

    def play_bonus_points_sound(self) -> None:
        """Plays sound when bonus points are awarded."""
        self.bonus_points_sound.play()

    def play_timer_warning_sound(self) -> None:
        """Plays sound when time is about to run out."""
        self.timer_warning_sound.play()