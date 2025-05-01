import pygame
import random
import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def get_elapsed_time(self):
        if self.start_time is not None:
            return str(round(self.elapsed_time + (time.time() - self.start_time), 2)) + " seconds"
        return str(round(self.elapsed_time, 2)) + " seconds"

class Difficulty:
    def __init__(self, level):
        self.level = level

    def get_puzzles(self):
        puzzles = {
            'easy': [
                "530070000\n" 
                "600195000\n"
                "098000060\n"
                "800060003\n"
                "400803001\n"
                "700020006\n"
                "060000280\n"
                "000419005\n"
                "000080079\n",
            ],
            'medium': [
                "002600000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n",
            ],
            'hard': [
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n"
                "000000000\n",
            ]
        }
        return puzzles.get(self.level, [])

class Grid:
    def __init__(self):
        self.cells = [[0 for _ in range(9)] for _ in range(9)]

    def validate(self):
        # Simplified validation logic for demonstration
        return True

    def fill_cell(self, row, col, symbol):
        self.cells[row][col] = symbol

    def is_full(self):
        return all(all(cell != 0 for cell in row) for row in self.cells)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = None

    def start_game(self):
        self.difficulty = Difficulty('easy')  # Example difficulty
        self.load_puzzle(self.difficulty.level)
        self.timer.start()
        # Game loop would go here

    def reset_game(self):
        self.grid = Grid()
        self.timer.stop()
        self.timer = Timer()
        self.start_game()

    def load_puzzle(self, difficulty):
        puzzles = self.difficulty.get_puzzles()
        if puzzles:
            puzzle = random.choice(puzzles)
            self.grid.cells = [list(map(int, row)) for row in puzzle.strip().split('\n')]

    def track_time(self):
        return self.timer.get_elapsed_time()