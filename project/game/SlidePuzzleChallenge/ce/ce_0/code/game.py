import pygame
import random
import time
from typing import List, Tuple

class Tile:
    def __init__(self, number: int, position: Tuple[int, int]):
        self.number = number
        self.position = position

    def slide(self) -> None:
        pass  # Placeholder for sliding logic

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> None:
        self.elapsed_time = int(time.time() - self.start_time)

    def get_time(self) -> int:
        return int(time.time() - self.start_time)

class Difficulty:
    def __init__(self):
        self.level = 1

    def set_level(self, level: int) -> None:
        self.level = level

    def get_level(self) -> int:
        return self.level

class Grid:
    def __init__(self):
        self.tiles: List[List[Tile]] = []

    def initialize_grid(self, size: int) -> None:
        self.tiles = [[Tile(j + i * size, (i, j)) for j in range(size)] for i in range(size)]
        self.tiles[-1][-1] = None  # Empty tile

    def update_tile_position(self, tile: Tile, new_position: Tuple[int, int]) -> None:
        tile.position = new_position

    def check_win_condition(self) -> bool:
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile and tile.number != (i * len(row) + j):
                    return False
        return True

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def start_game(self) -> None:
        self.grid.initialize_grid(self.difficulty.get_level())
        self.timer.start()

    def shuffle_tiles(self) -> None:
        flat_tiles = [tile for row in self.grid.tiles for tile in row if tile]
        random.shuffle(flat_tiles)
        size = self.difficulty.get_level()
        for i in range(size):
            for j in range(size):
                if i * size + j < len(flat_tiles):
                    self.grid.tiles[i][j] = flat_tiles[i * size + j]
                else:
                    self.grid.tiles[i][j] = None

    def slide_tile(self, tile: Tile) -> None:
        empty_tile_position = next((i, j) for i, row in enumerate(self.grid.tiles)
                                    for j, t in enumerate(row) if t is None)
        if self.is_adjacent(tile.position, empty_tile_position):
            self.grid.update_tile_position(tile, empty_tile_position)

    def is_adjacent(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        return (abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]) or \
               (abs(pos1[1] - pos2[1]) == 1 and pos1[0] == pos2[0])

    def save_progress(self) -> None:
        with open('game_progress.txt', 'w') as f:
            f.write(f"{self.timer.get_time()}\n")
            f.write(f"{self.difficulty.get_level()}\n")
            for row in self.grid.tiles:
                f.write('|'.join(str(tile.number) if tile else 'None' for tile in row) + '\n')

    def load_progress(self) -> None:
        with open('game_progress.txt', 'r') as f:
            lines = f.readlines()
            self.timer.elapsed_time = int(lines[0].strip())
            self.difficulty.set_level(int(lines[1].strip()))
            self.grid.tiles = []
            for line in lines[2:]:
                row = []
                for number in line.strip().split('|'):
                    if number == 'None':
                        row.append(None)
                    else:
                        row.append(Tile(int(number), (len(self.grid.tiles), len(row))))
                self.grid.tiles.append(row)

    def provide_hint(self) -> str:
        # Simple hint logic (could be more complex)
        if self.grid.check_win_condition():
            return "You have already won!"
        return "Try moving the tile with number X."

    def reset_game(self) -> None:
        self.grid.initialize_grid(self.difficulty.get_level())
        self.timer.stop()
        self.timer.start()