import pygame
import random
import time

class Tile:
    def __init__(self, value):
        self.value = value

class Grid:
    def __init__(self, size):
        self.size = size
        self.tiles = self.create_tiles()
        self.shuffle_tiles()

    def create_tiles(self):
        return [Tile(i) for i in range(1, self.size**2)] + [Tile(0)]  # 0 represents the empty tile

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def slide_tile(self, tile):
        # Logic to slide the tile into the empty space
        empty_index = self.tiles.index(Tile(0))
        tile_index = self.tiles.index(tile)

        if self.is_adjacent(empty_index, tile_index):
            self.tiles[empty_index], self.tiles[tile_index] = self.tiles[tile_index], self.tiles[empty_index]
            return True
        return False

    def is_adjacent(self, empty_index, tile_index):
        # Check if the tile is adjacent to the empty tile
        empty_row, empty_col = divmod(empty_index, self.size)
        tile_row, tile_col = divmod(tile_index, self.size)
        return (abs(empty_row - tile_row) == 1 and empty_col == tile_col) or (empty_row == tile_row and abs(empty_col - tile_col) == 1)

    def is_solved(self):
        return all(self.tiles[i].value == i + 1 for i in range(len(self.tiles) - 1)) and self.tiles[-1].value == 0

class Timer:
    def __init__(self):
        self.time_elapsed = 0
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            self.time_elapsed = time.time() - self.start_time
            self.start_time = None
        return int(self.time_elapsed)

class Settings:
    def __init__(self):
        self.difficulty = "easy"

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as file:
                self.difficulty = file.read().strip()
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        with open('settings.txt', 'w') as file:
            file.write(self.difficulty)

class Game:
    def __init__(self):
        self.grid = Grid(size=4)
        self.timer = Timer()
        self.settings = Settings()

    def start_game(self, difficulty: str):
        self.settings.difficulty = difficulty
        self.timer.start_timer()

    def save_progress(self):
        with open('game_state.txt', 'w') as file:
            file.write(f"{self.grid.tiles}\n{self.timer.stop_timer()}")

    def load_progress(self):
        try:
            with open('game_state.txt', 'r') as file:
                lines = file.readlines()
                self.grid.tiles = eval(lines[0].strip())
                self.timer.time_elapsed = int(lines[1].strip())
        except FileNotFoundError:
            print("No saved game found.")

    def provide_hint(self) -> str:
        # Logic for providing hints
        return "Hint: Move the tile with value 1."

    def reset_game(self):
        self.grid = Grid(size=4)
        self.timer = Timer()
        self.settings.load_settings()