import random
from typing import List

class Difficulty:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.elapsed_time = 0.0

    def start(self) -> None:
        import time
        self.start_time = time.time()

    def stop(self) -> float:
        import time
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

class Grid:
    def __init__(self):
        self.cells: List[List[str]] = [["" for _ in range(9)] for _ in range(9)]

    def set_cell(self, row: int, col: int, symbol: str) -> bool:
        if self.is_valid_move(row, col, symbol):
            self.cells[row][col] = symbol
            return True
        return False

    def get_cell(self, row: int, col: int) -> str:
        return self.cells[row][col]

    def is_valid(self) -> bool:
        # Implement Sudoku validation logic
        return True

    def is_valid_move(self, row: int, col: int, symbol: str) -> bool:
        # Implement logic to check if placing the symbol is valid
        return True

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = None

    def start_game(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.load_puzzle(difficulty)
        self.timer.start()

    def reset_game(self) -> None:
        self.grid = Grid()
        self.timer = Timer()

    def input_symbol(self, row: int, col: int, symbol: str) -> bool:
        return self.grid.set_cell(row, col, symbol)

    def check_solution(self) -> bool:
        return self.grid.is_valid()

    def load_puzzle(self, difficulty: Difficulty) -> None:
        puzzles = self.load_puzzles_from_file()
        puzzle = puzzles.get(difficulty)
        if puzzle:
            for r in range(9):
                for c in range(9):
                    if puzzle[r][c] != "":
                        self.grid.set_cell(r, c, puzzle[r][c])

    def load_puzzles_from_file(self) -> dict:
        puzzles = {
            Difficulty.EASY: [
                ["5", "3", "", "", "7", "", "", "", ""],
                ["6", "", "", "1", "9", "5", "", "", ""],
                ["", "9", "8", "", "", "", "", "6", ""],
                ["8", "", "", "", "6", "", "", "", "3"],
                ["4", "", "", "8", "", "3", "", "", "1"],
                ["7", "", "", "", "2", "", "", "", "6"],
                ["", "6", "", "", "", "", "2", "8", ""],
                ["", "", "", "4", "1", "9", "", "", "5"],
                ["", "", "", "", "8", "", "", "7", "9"]
            ],
            Difficulty.MEDIUM: [
                ["8", "5", "", "", "", "2", "", "", "1"],
                ["", "", "3", "6", "", "8", "", "", "4"],
                ["", "9", "", "", "7", "", "5", "", ""],
                ["4", "", "", "8", "", "3", "", "", "6"],
                ["7", "", "1", "", "5", "", "", "", "3"],
                ["6", "", "", "2", "", "9", "", "", "8"],
                ["", "", "8", "", "6", "", "", "2", ""],
                ["5", "", "", "1", "", "7", "4", "", ""],
                ["3", "", "", "", "", "4", "", "5", "9"]
            ],
            Difficulty.HARD: [
                ["", "2", "", "1", "", "7", "", "3", "9"],
                ["", "", "6", "", "8", "", "", "", "1"],
                ["", "", "", "", "4", "3", "", "", "5"],
                ["", "5", "3", "", "", "1", "7", "", ""],
                ["", "1", "", "", "", "", "", "4", ""],
                ["", "", "4", "3", "", "", "1", "2", ""],
                ["1", "", "", "7", "5", "", "", "", ""],
                ["8", "", "", "", "", "", "3", "", ""],
                ["9", "4", "", "6", "", "2", "", "1", ""]
            ]
        }
        return puzzles