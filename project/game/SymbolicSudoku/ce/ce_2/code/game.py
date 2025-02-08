import pygame
import time
from typing import List

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.elapsed_time = 0.0

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> float:
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

class Difficulty:
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Grid:
    def __init__(self):
        self.cells: List[List[str]] = [['.' for _ in range(9)] for _ in range(9)]

    def display(self) -> None:
        for row in self.cells:
            print(" ".join(row))

    def input_symbol(self, row: int, col: int, symbol: str) -> bool:
        if self.cells[row][col] == '.':
            self.cells[row][col] = symbol
            return True
        return False

    def validate(self) -> bool:
        # Placeholder for validation logic
        return True

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self, difficulty: str = Difficulty.easy) -> None:
        self.difficulty = difficulty
        self.timer.start()
        self.load_puzzle()
        self.grid.display()

    def reset_game(self) -> None:
        self.grid = Grid()
        self.timer = Timer()
        self.start_game(self.difficulty)

    def load_puzzle(self) -> None:
        with open('puzzles.txt', 'r') as file:
            puzzle = file.readline().strip().split()
            for i in range(9):
                self.grid.cells[i] = list(puzzle[i])

    def track_time(self) -> None:
        elapsed = self.timer.stop()
        print(f"Time taken: {elapsed:.2f} seconds")