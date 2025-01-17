import pygame
import time
from typing import List

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> float:
        return time.time() - self.start_time

class Difficulty:
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Grid:
    def __init__(self):
        self.cells: List[List[str]] = [['' for _ in range(9)] for _ in range(9)]

    def fill_cell(self, row: int, col: int, symbol: str) -> None:
        self.cells[row][col] = symbol

    def validate(self) -> bool:
        # Basic validation logic for Sudoku
        # This function can be expanded with full Sudoku validation rules
        return True

    def is_complete(self) -> bool:
        return all(all(cell != '' for cell in row) for row in self.cells)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.load_puzzle(f"{difficulty}_puzzles.txt")
        self.timer.start()

    def reset_game(self) -> None:
        self.grid = Grid()
        self.timer = Timer()

    def load_puzzle(self, file_name: str) -> None:
        with open(file_name, 'r') as file:
            for row_index, line in enumerate(file):
                symbols = line.strip().split('|')
                for col_index, symbol in enumerate(symbols):
                    self.grid.fill_cell(row_index, col_index, symbol)

    def track_time(self) -> None:
        elapsed_time = self.timer.stop()
        print(f"Time taken: {elapsed_time:.2f} seconds")