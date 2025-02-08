import pygame
import random

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int) -> None:
        self.time_remaining = duration

    def update(self) -> None:
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self) -> bool:
        return self.time_remaining <= 0


class Grid:
    def __init__(self, size: int):
        self.tiles = []
        self.create_grid(size)

    def create_grid(self, size: int) -> None:
        self.tiles = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]

    def get_adjacent_tiles(self, x: int, y: int) -> list[tuple[int, int]]:
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.tiles) and 0 <= ny < len(self.tiles):
                adjacent.append((nx, ny))
        return adjacent


class Game:
    def __init__(self):
        self.grid = Grid(size=5)
        self.timer = Timer()
        self.current_level = 1

    def start_game(self, level: int) -> None:
        self.current_level = level
        self.timer.start_timer(60)  # Start with 60 seconds timer

    def update_timer(self) -> None:
        self.timer.update()

    def check_path(self, path: list) -> bool:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            if (x2, y2) not in self.grid.get_adjacent_tiles(x1, y1):
                return False
            if self.grid.tiles[x2][y2] != self.grid.tiles[x1][y1] + 1:
                return False
        return True