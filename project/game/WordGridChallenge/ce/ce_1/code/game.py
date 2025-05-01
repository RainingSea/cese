import pygame
from grid import Grid
from score_manager import ScoreManager
from timer import Timer

class GameEngine:
    def __init__(self):
        self.grid = Grid()
        self.score_manager = ScoreManager()
        self.timer = Timer()

    def start_game(self):
        self.timer.start()
        self.grid.generate_grid(size=4)  # Example size
        self.grid.display_grid()
        # Game loop and event handling would go here

    def check_word(self, word: str) -> bool:
        return word in self.score_manager.load_word_list()

    def update_score(self):
        # Logic to update score based on valid words found
        pass