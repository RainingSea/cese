import pygame
import time

class Game:
    def __init__(self):
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.start_time = time.time()
        self.winner = None

    def play_move(self, position: tuple) -> bool:
        if self.grid[position[1]][position[0]] == '' and self.winner is None:
            self.grid[position[1]][position[0]] = self.current_turn
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return True
        return False

    def check_winner(self) -> str:
        for row in self.grid:
            if row[0] == row[1] == row[2] != '':
                self.winner = row[0]
                return f"{self.winner} wins!"
        
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != '':
                self.winner = self.grid[0][col]
                return f"{self.winner} wins!"
        
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != '':
            self.winner = self.grid[0][0]
            return f"{self.winner} wins!"
        
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != '':
            self.winner = self.grid[0][2]
            return f"{self.winner} wins!"
        
        if all(cell != '' for row in self.grid for cell in row):
            return "Draw!"
        
        return ''

    def reset_game(self) -> None:
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.start_time = time.time()
        self.winner = None

    def draw(self, screen) -> None:
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, (0, 0, 0), (col * 100, row * 100, 100, 100), 1)
                if self.grid[row][col] == 'X':
                    pygame.draw.line(screen, (255, 0, 0), (col * 100 + 10, row * 100 + 10), (col * 100 + 90, row * 100 + 90), 5)
                    pygame.draw.line(screen, (255, 0, 0), (col * 100 + 90, row * 100 + 10), (col * 100 + 10, row * 100 + 90), 5)
                elif self.grid[row][col] == 'O':
                    pygame.draw.circle(screen, (0, 0, 255), (col * 100 + 50, row * 100 + 50), 40, 5)

    def save_result(self, winner: str, duration: float) -> None:
        with open('results.txt', 'a') as file:
            file.write(f"{winner}|wins|{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")

    def get_duration(self) -> float:
        return time.time() - self.start_time