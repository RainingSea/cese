import pygame
import json

class Game:
    def __init__(self) -> None:
        self.grid = [['' for _ in range(5)] for _ in range(5)]  # 5x5 grid
        self.score = 0
        self.history = []

    def display_grid(self) -> None:
        # Code to display the grid using Pygame
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                # Display each block (placeholder for actual rendering)
                print(f"Block at ({row}, {col}): {self.grid[row][col]}")

    def connect_blocks(self, positions: list[tuple[int, int]]) -> None:
        if not positions:
            return
        color = self.grid[positions[0][0]][positions[0][1]]
        for pos in positions:
            self.grid[pos[0]][pos[1]] = color
        self.update_score(len(positions))

    def update_score(self, num_blocks: int) -> None:
        self.score += num_blocks

    def undo_move(self) -> None:
        if self.history:
            self.grid = self.history.pop()

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            json.dump({'grid': self.grid, 'score': self.score}, f)

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                data = json.load(f)
                self.grid = data['grid']
                self.score = data['score']
        except FileNotFoundError:
            print("No saved game state found.")