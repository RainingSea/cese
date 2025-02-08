import pygame
import os

class Game:
    def __init__(self) -> None:
        self.grid = [[0 for _ in range(10)] for _ in range(10)]  # 10x10 grid
        self.score = 0
        self.undo_stack = []
        self.load_game_state()

    def draw_grid(self) -> None:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                color = (255, 255, 255) if self.grid[row][col] == 0 else (0, 255, 0)
                pygame.draw.rect(screen, color, (col * 50, row * 50, 50, 50))

    def select_block(self, x: int, y: int) -> None:
        if 0 <= x < 10 and 0 <= y < 10:
            self.undo_stack.append((self.grid[x][y], x, y))  # Save the state before change
            self.grid[x][y] = 1 if self.grid[x][y] == 0 else 0  # Toggle block state

    def clear_blocks(self, blocks: list[tuple]) -> None:
        for x, y in blocks:
            self.grid[x][y] = 0
        self.update_score(len(blocks))

    def update_score(self, count: int) -> None:
        self.score += count

    def fall_blocks(self) -> None:
        for col in range(len(self.grid[0])):
            for row in range(len(self.grid) - 1, -1, -1):
                if self.grid[row][col] == 0 and row > 0:
                    for r in range(row, 0, -1):
                        self.grid[r][col] = self.grid[r - 1][col]
                    self.grid[0][col] = 0

    def undo_move(self) -> None:
        if self.undo_stack:
            last_move = self.undo_stack.pop()
            self.grid[last_move[1]][last_move[2]] = last_move[0]  # Restore previous state

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.score}\n")
            for row in self.grid:
                f.write(' '.join(map(str, row)) + '\n')

    def load_game_state(self) -> None:
        if os.path.exists('game_state.txt'):
            with open('game_state.txt', 'r') as f:
                self.score = int(f.readline().strip())
                for i, line in enumerate(f):
                    self.grid[i] = list(map(int, line.strip().split()))