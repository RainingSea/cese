import pygame
import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()
        self.elapsed_time = 0  # Initialize elapsed_time when starting

    def stop(self):
        self.elapsed_time = time.time() - self.start_time

    def get_elapsed_time(self) -> int:
        return int(time.time() - self.start_time)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)  # Method to return position as a tuple

class Player:
    def __init__(self):
        self.position = Position(0, 0)
        self.score = 0

    def move(self, direction):
        if direction == "up":
            self.position.y -= 1
        elif direction == "down":
            self.position.y += 1
        elif direction == "left":
            self.position.x -= 1
        elif direction == "right":
            self.position.x += 1

    def collect_star(self, maze):
        current_tile = maze.grid[self.position.y][self.position.x]
        if current_tile.tile_type == 'S':  # Assuming 'S' represents a star
            self.score += 1
            current_tile.tile_type = '0'  # Change star to empty after collection

class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type

class Maze:
    def __init__(self):
        self.grid = []

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                row = [Tile(char) for char in line.strip()]
                self.grid.append(row)

    def move_tile(self, x, y, direction):
        if direction == "up" and y > 0:
            self.grid[y-1][x], self.grid[y][x] = self.grid[y][x], self.grid[y-1][x]
            return True
        elif direction == "down" and y < len(self.grid) - 1:
            self.grid[y+1][x], self.grid[y][x] = self.grid[y][x], self.grid[y+1][x]
            return True
        elif direction == "left" and x > 0:
            self.grid[y][x-1], self.grid[y][x] = self.grid[y][x], self.grid[y][x-1]
            return True
        elif direction == "right" and x < len(self.grid[y]) - 1:
            self.grid[y][x+1], self.grid[y][x] = self.grid[y][x], self.grid[y][x+1]
            return True
        return False

    def check_win(self, player):
        end_tile = self.grid[player.position.y][player.position.x]
        return end_tile.tile_type == 'E'  # Assuming 'E' represents the end tile

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int):
        self.points += points

    def get_score(self) -> int:
        return self.points

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()
        self.score = Score()

    def start_game(self):
        self.load_level(1)
        self.timer.start()
        # Main game loop would go here

    def reset_maze(self):
        self.maze = Maze()
        self.load_level(1)
        self.player.position = Position(0, 0)  # Reset player position

    def load_level(self, level):
        filename = f"mazes_level{level}.txt"
        self.maze.load_from_file(filename)

    def check_win(self):
        return self.maze.check_win(self.player)