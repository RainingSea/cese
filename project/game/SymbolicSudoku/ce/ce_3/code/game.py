import pygame
import time

class Difficulty:
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.elapsed_time = 0.0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

class Grid:
    def __init__(self):
        self.cells = [['' for _ in range(9)] for _ in range(9)]

    def initialize_grid(self, puzzle: str):
        for i, line in enumerate(puzzle.strip().split('\n')):
            self.cells[i] = list(line)

    def is_valid(self, row: int, col: int, symbol: str) -> bool:
        for i in range(9):
            if self.cells[row][i] == symbol or self.cells[i][col] == symbol:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.cells[i][j] == symbol:
                    return False
        return True

    def display(self) -> None:
        for row in self.cells:
            print(' '.join(row))

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = Difficulty.EASY

    def start_game(self, difficulty: Difficulty = Difficulty.EASY) -> None:
        self.difficulty = difficulty
        self.load_puzzle()
        self.timer.start()
        self.grid.display()

    def reset_game(self) -> None:
        self.grid = Grid()
        self.start_game(self.difficulty)

    def input_symbol(self, row: int, col: int, symbol: str) -> bool:
        if self.grid.is_valid(row, col, symbol):
            self.grid.cells[row][col] = symbol
            return True
        return False

    def check_solution(self) -> bool:
        # Check if the grid is completely filled and valid
        for row in self.grid.cells:
            if '' in row:
                return False
        return True

    def load_puzzle(self) -> None:
        with open('easy_puzzles.txt', 'r') as file:
            puzzle = file.readline()
            self.grid.initialize_grid(puzzle)