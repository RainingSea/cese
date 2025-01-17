import pygame
import random

class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points: int) -> None:
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score


class Level:
    def __init__(self):
        self.difficulty = 1

    def next_level(self) -> None:
        self.difficulty += 1

    def get_difficulty(self) -> int:
        return self.difficulty


class Grid:
    def __init__(self, size: int):
        self.blocks = []
        self.size = size
        self.initialize_grid()

    def initialize_grid(self) -> None:
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        self.blocks = [[random.choice(colors) for _ in range(self.size)] for _ in range(self.size)]

    def get_block_color(self, position: tuple) -> str:
        x, y = position
        return self.blocks[y][x]

    def is_path_clear(self, start: tuple, end: tuple) -> bool:
        # Placeholder for pathfinding logic
        return True


class Game:
    def __init__(self):
        self.grid = Grid(size=5)
        self.score = Score()
        self.level = Level()

    def start_game(self) -> None:
        print("Game Started")

    def draw_grid(self) -> None:
        for row in self.grid.blocks:
            print(" | ".join(row))

    def check_connection(self, start: tuple, end: tuple) -> bool:
        return self.grid.is_path_clear(start, end)

    def clear_blocks(self, start: tuple, end: tuple) -> None:
        # Logic to clear blocks
        self.score.update_score(10)  # Example score update
        print(f"Cleared blocks from {start} to {end}")