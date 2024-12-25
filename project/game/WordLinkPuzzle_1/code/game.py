import pygame
import random

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int):
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def display_grid(self):
        # Initialize Pygame display
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 36)
        cell_size = 40
        
        for row_index, row in enumerate(self.letters):
            for col_index, letter in enumerate(row):
                text_surface = font.render(letter, True, (255, 255, 255))
                screen.blit(text_surface, (col_index * cell_size, row_index * cell_size))
        
        pygame.display.flip()

    def validate_word(self, word: str) -> bool:
        with open('dictionary.txt', 'r') as file:
            dictionary = file.read().splitlines()
        return word.upper() in dictionary  # Ensure case-insensitive comparison

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, word: str) -> int:
        base_score = len(word)  # Base score based on word length
        bonus_points = 0
        
        # Bonus points for rare words (for demonstration, let's assume words longer than 5 are rare)
        if len(word) > 5:
            bonus_points = 5  # Arbitrary bonus for longer words
        return base_score + bonus_points

    def add_points(self, points: int):
        self.points += points

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self):
        self.time_left = 0
        self.is_paused = False

    def start_timer(self, duration: int):
        self.time_left = duration
        self.is_paused = False

    def pause_timer(self):
        self.is_paused = True

    def resume_timer(self):
        self.is_paused = False

    def update_timer(self):
        if not self.is_paused and self.time_left > 0:
            self.time_left -= 1  # Decrement time left by 1 second

    def check_time(self) -> bool:
        return self.time_left > 0

class WordList:
    def __init__(self):
        self.words = []

    def add_word(self, word: str):
        self.words.append(word)

    def get_words(self) -> list:
        return self.words

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.formed_words = WordList()
        self.sound_effects = {
            "word_formed": pygame.mixer.Sound("sounds/word_formed.wav"),
            "bonus_points": pygame.mixer.Sound("sounds/bonus_points.wav"),
            "timer_warning": pygame.mixer.Sound("sounds/timer_warning.wav"),
        }

    def start_game(self, difficulty: str):
        size = 4 if difficulty == 'Easy' else 6 if difficulty == 'Medium' else 8
        self.grid.generate_grid(size)
        self.timer.start_timer(60)  # 60 seconds for each game
        self.grid.display_grid()  # Display the grid when the game starts

    def pause_game(self):
        self.timer.pause_timer()

    def save_game(self):
        with open('game_state.txt', 'w') as file:
            file.write(f"{self.grid.letters}\n{self.score.get_score()}\n{self.timer.time_left}\n{self.formed_words.get_words()}")

    def load_game(self):
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.grid.letters = eval(lines[0].strip())
            self.score.points = int(lines[1].strip())
            self.timer.time_left = int(lines[2].strip())
            self.formed_words.words = eval(lines[3].strip())

    def play_sound(self, event: str):
        if event in self.sound_effects:
            self.sound_effects[event].play()