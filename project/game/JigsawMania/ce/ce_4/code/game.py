import pygame
import json
from puzzles import Puzzle
from timer import Timer
from user_progress import UserProgress

class Game:
    def __init__(self):
        self.puzzle = None
        self.timer = Timer()
        self.user_progress = UserProgress()

    def start_game(self, image_path: str, difficulty: str) -> None:
        self.puzzle = Puzzle()
        self.puzzle.create_puzzle(image_path, difficulty)
        self.timer.start()
        # Additional game logic to display the puzzle and handle user input goes here

    def save_progress(self) -> None:
        data = {
            'puzzle_state': self.puzzle.get_state(),
            'time_elapsed': self.timer.stop(),
        }
        self.user_progress.save(data)

    def load_progress(self) -> None:
        data = self.user_progress.load()
        self.puzzle.load_state(data['puzzle_state'])
        self.timer.start_time = data['time_elapsed']

    def restart_game(self) -> None:
        self.puzzle = None
        self.start_game('puzzles.txt', 'settings.txt')