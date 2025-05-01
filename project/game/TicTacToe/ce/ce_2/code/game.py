import pygame
import os
import time

class Game:
    def __init__(self):
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.timer = 0.0
        self.start_time = None
        self.font = pygame.font.Font(None, 74)
        self.result_font = pygame.font.Font(None, 36)

    def start_game(self):
        self.reset_game()
        self.start_time = time.time()

    def make_move(self, x: int, y: int):
        if self.grid[y][x] == '':
            self.grid[y][x] = self.current_player
            winner = self.check_winner()
            if winner:
                self.save_results(winner, time.time() - self.start_time)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self) -> str:
        for row in self.grid:
            if row[0] == row[1] == row[2] != '':
                return f'Player {row[0]} wins!'
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != '':
                return f'Player {self.grid[0][col]} wins!'
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != '':
            return f'Player {self.grid[0][0]} wins!'
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != '':
            return f'Player {self.grid[0][2]} wins!'
        if all(cell != '' for row in self.grid for cell in row):
            return 'Draw!'
        return None

    def reset_game(self):
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.timer = 0.0

    def save_results(self, outcome: str, duration: float):
        with open('game_results.txt', 'a') as file:
            file.write(f'{outcome}|{duration:.2f}\n')

    def update_display(self):
        screen = pygame.display.set_mode((300, 400))
        screen.fill((255, 255, 255))
        for y in range(3):
            for x in range(3):
                pygame.draw.rect(screen, (0, 0, 0), (x * 100, y * 100, 100, 100), 1)
                if self.grid[y][x] != '':
                    text = self.font.render(self.grid[y][x], True, (0, 0, 0))
                    screen.blit(text, (x * 100 + 30, y * 100 + 10))
        if self.start_time:
            self.timer = time.time() - self.start_time
        timer_text = self.result_font.render(f'Time: {self.timer:.2f}', True, (0, 0, 0))
        screen.blit(timer_text, (10, 320))

        winner = self.check_winner()
        if winner:
            result_text = self.result_font.render(winner, True, (0, 0, 0))
            screen.blit(result_text, (10, 350))