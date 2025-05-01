import pygame
import time

class Game:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.timer = 0
        self.start_time = None

    def start_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.timer = 0
        self.start_time = time.time()

    def make_move(self, x: int, y: int) -> None:
        if self.board[y][x] == '':
            self.board[y][x] = self.current_turn
            winner = self.check_winner()
            if winner:
                self.save_result(winner, int(time.time() - self.start_time))
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    def check_winner(self) -> str:
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        if all(cell != '' for row in self.board for cell in row):
            return 'Draw'
        return None

    def restart_game(self) -> None:
        self.start_game()

    def save_result(self, winner: str, duration: int) -> None:
        with open('results.txt', 'a') as f:
            f.write(f'{winner}|{duration}\n')

    def draw(self, screen) -> None:
        for y in range(3):
            for x in range(3):
                rect = pygame.Rect(x * 100, y * 100, 100, 100)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                if self.board[y][x] == 'X':
                    pygame.draw.line(screen, (255, 0, 0), (x * 100, y * 100), (x * 100 + 100, y * 100 + 100), 3)
                    pygame.draw.line(screen, (255, 0, 0), (x * 100 + 100, y * 100), (x * 100, y * 100 + 100), 3)
                elif self.board[y][x] == 'O':
                    pygame.draw.circle(screen, (0, 0, 255), (x * 100 + 50, y * 100 + 50), 40, 3)