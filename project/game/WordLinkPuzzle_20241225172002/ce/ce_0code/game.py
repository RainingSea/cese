import random
import pygame

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int):
        """Generates a grid of random uppercase letters."""
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def display_grid(self, screen):
        """Displays the grid on the Pygame surface."""
        font = pygame.font.Font(None, 36)
        for i, row in enumerate(self.letters):
            for j, letter in enumerate(row):
                text = font.render(letter, True, (0, 0, 0))
                screen.blit(text, (j * 40 + 50, i * 40 + 50))  # Adjust position as needed

    def connect_letters(self, start: tuple, end: tuple):
        """Logic to connect letters from start to end."""
        # Placeholder for actual connection logic
        return []  # This should return the letters connected

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, word: str) -> int:
        """Calculates score based on the length of the word."""
        base_score = len(word)
        # Add bonus for rare words (placeholder logic)
        if len(word) > 5:
            base_score += 2  # Bonus for longer words
        self.points += base_score  # Update cumulative score
        return base_score

    def get_score(self) -> int:
        """Returns the current score."""
        return self.points

class Timer:
    def __init__(self):
        self.time_left = 0
        self.paused = False
        self.remaining_time = 0

    def start_timer(self, duration: int):
        """Starts the timer with a specified duration."""
        self.time_left = duration
        self.remaining_time = duration
        self.paused = False

    def pause_timer(self):
        """Pauses the timer."""
        if not self.paused:
            self.remaining_time = self.time_left
            self.paused = True

    def resume_timer(self):
        """Resumes the timer."""
        if self.paused:
            self.time_left = self.remaining_time
            self.paused = False

    def update_timer(self):
        """Updates the timer, reducing time left if not paused."""
        if not self.paused and self.time_left > 0:
            self.time_left -= 1  # Assuming this is called every second

    def check_time(self) -> bool:
        """Checks if there is time left."""
        return self.time_left > 0

class WordList:
    def __init__(self):
        self.words = []
        self.load_dictionary()

    def load_dictionary(self):
        """Loads the dictionary from the file for word validation."""
        self.valid_words = set()
        with open('dictionary.txt', 'r') as f:
            for line in f:
                self.valid_words.add(line.strip().upper())  # Store words in uppercase for consistency

    def add_word(self, word: str):
        """Adds a word to the list of formed words."""
        if word.upper() in self.valid_words:  # Validate the word before adding
            self.words.append(word)

    def get_words(self) -> list:
        """Returns the list of formed words."""
        return self.words

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.formed_words = WordList()
        self.sounds = self.load_sounds()

    def load_sounds(self):
        """Loads sound effects for the game."""
        sounds = {
            "word_formed": pygame.mixer.Sound("sounds/word_formed.wav"),
            "bonus_points": pygame.mixer.Sound("sounds/bonus_points.wav"),
            "timer_warning": pygame.mixer.Sound("sounds/timer_warning.wav"),
        }
        return sounds

    def start_game(self):
        """Starts the game by generating the grid and starting the timer."""
        self.grid.generate_grid(4)  # Example grid size
        self.timer.start_timer(60)  # Start timer for 60 seconds

    def pause_game(self):
        """Pauses the game."""
        self.timer.pause_timer()

    def save_progress(self):
        """Saves the current game progress to a file."""
        with open('game_progress.txt', 'w') as f:
            f.write(f"{self.grid.letters}|{self.score.get_score()}|{self.timer.time_left}|{self.formed_words.get_words()}")

    def load_progress(self):
        """Loads the game progress from a file."""
        with open('game_progress.txt', 'r') as f:
            data = f.read().split('|')
            self.grid.letters = eval(data[0])
            self.score.points = int(data[1])
            self.timer.time_left = int(data[2])
            self.formed_words.words = eval(data[3])

    def play_sound(self, event: str):
        """Plays sound based on the game event."""
        if event in self.sounds:
            self.sounds[event].play()