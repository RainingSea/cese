import pygame
import time

class Game:
    def __init__(self) -> None:
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.timer = 0.0
        self.start_time = None

    def play_move(self, row: int, col: int) -> str:
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            winner = self.check_winner()
            self.current_player = "O" if self.current_player == "X" else "X"
            return winner
        return "Invalid move"

    def check_winner(self) -> str:
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return f"{self.board[row][0]} wins!"
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return f"{self.board[0][col]} wins!"
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return f"{self.board[0][0]} wins!"
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return f"{self.board[0][2]} wins!"

        if all(cell != "" for row in self.board for cell in row):
            return "It's a draw!"

        return "Continue playing"

    def reset_game(self) -> None:
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.timer = 0.0
        self.start_time = None

    def start_timer(self) -> None:
        self.start_time = time.time()

    def stop_timer(self) -> float:
        if self.start_time is not None:
            self.timer = time.time() - self.start_time
            self.start_time = None
        return self.timer

    def save_game_data(self) -> None:
        with open('game_data.txt', 'w') as f:
            for row in self.board:
                f.write('|'.join(row) + '\n')
            f.write(self.current_player + '\n')

    def load_game_data(self) -> None:
        try:
            with open('game_data.txt', 'r') as f:
                lines = f.readlines()
                self.board = [line.strip().split('|') for line in lines[:-1]]
                self.current_player = lines[-1].strip()
        except FileNotFoundError:
            self.reset_game()