import pygame
import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> str:
        elapsed_time = time.time() - self.start_time
        return f"{int(elapsed_time)} seconds"

class Player:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_symbol(self) -> str:
        return self.symbol

class Grid:
    def __init__(self):
        self.cells = [['' for _ in range(3)] for _ in range(3)]

    def update_cell(self, row: int, col: int, symbol: str):
        self.cells[row][col] = symbol

    def is_full(self) -> bool:
        return all(cell != '' for row in self.cells for cell in row)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.current_player = Player('X')
        self.winner = None

    def start_game(self):
        self.timer.start()
        self.winner = None
        self.grid = Grid()
        self.run_game_loop()

    def run_game_loop(self):
        # Placeholder for the main game loop
        pass

    def make_move(self, row: int, col: int):
        if self.grid.cells[row][col] == '' and not self.winner:
            self.grid.update_cell(row, col, self.current_player.get_symbol())
            self.check_winner()
            self.current_player = Player('O' if self.current_player.get_symbol() == 'X' else 'X')

    def check_winner(self) -> str:
        for row in range(3):
            if self.grid.cells[row][0] == self.grid.cells[row][1] == self.grid.cells[row][2] != '':
                self.winner = self.grid.cells[row][0]
                return f"{self.winner} wins"

        for col in range(3):
            if self.grid.cells[0][col] == self.grid.cells[1][col] == self.grid.cells[2][col] != '':
                self.winner = self.grid.cells[0][col]
                return f"{self.winner} wins"

        if self.grid.cells[0][0] == self.grid.cells[1][1] == self.grid.cells[2][2] != '':
            self.winner = self.grid.cells[0][0]
            return f"{self.winner} wins"

        if self.grid.cells[0][2] == self.grid.cells[1][1] == self.grid.cells[2][0] != '':
            self.winner = self.grid.cells[0][2]
            return f"{self.winner} wins"

        if self.grid.is_full():
            return "Draw"

    def restart_game(self):
        self.start_game()