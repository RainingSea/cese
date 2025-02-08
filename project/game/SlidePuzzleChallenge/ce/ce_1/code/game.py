import pygame
import random
import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time

    def get_elapsed_time(self):
        return int(self.elapsed_time)

class Grid:
    def __init__(self, size):
        self.tiles = list(range(size * size))
        self.size = size
        self.empty_tile = self.tiles[-1]

    def display(self):
        for i in range(self.size):
            print(self.tiles[i * self.size:(i + 1) * self.size])

    def slide_tile(self, direction):
        empty_index = self.tiles.index(self.empty_tile)
        if direction == 'up' and empty_index + self.size < len(self.tiles):
            self.tiles[empty_index], self.tiles[empty_index + self.size] = self.tiles[empty_index + self.size], self.tiles[empty_index]
        elif direction == 'down' and empty_index - self.size >= 0:
            self.tiles[empty_index], self.tiles[empty_index - self.size] = self.tiles[empty_index - self.size], self.tiles[empty_index]
        elif direction == 'left' and (empty_index + 1) % self.size != 0:
            self.tiles[empty_index], self.tiles[empty_index + 1] = self.tiles[empty_index + 1], self.tiles[empty_index]
        elif direction == 'right' and empty_index % self.size != 0:
            self.tiles[empty_index], self.tiles[empty_index - 1] = self.tiles[empty_index - 1], self.tiles[empty_index]

    def check_win(self):
        return self.tiles == list(range(len(self.tiles)))

class Game:
    def __init__(self):
        self.grid = Grid(4)
        self.timer = Timer()
        self.difficulty = 1

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.shuffle_tiles()
        self.timer.start()

    def shuffle_tiles(self):
        random.shuffle(self.grid.tiles)

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write('|'.join(map(str, self.grid.tiles)) + '\n')
            f.write(str(self.timer.get_elapsed_time()) + '\n')

    def load_progress(self):
        with open('progress.txt', 'r') as f:
            lines = f.readlines()
            self.grid.tiles = list(map(int, lines[0].strip().split('|')))
            self.timer.elapsed_time = int(lines[1].strip())

    def get_hint(self):
        return "Try sliding the tile in the direction of the empty space."

    def reset_game(self):
        self.grid = Grid(4)
        self.timer = Timer()