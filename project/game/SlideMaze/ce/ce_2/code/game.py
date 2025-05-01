import pygame
import time

class Game:
    def __init__(self):
        self.maze = None
        self.timer = Timer()
        self.score = Score()

    def start_game(self):
        self.load_level(1)
        self.timer.start()
        # Main game loop goes here

    def reset_maze(self):
        self.load_level(self.maze.level_id)

    def load_level(self, level_id: int):
        with open('mazes.txt', 'r') as f:
            mazes = f.readlines()
        maze_data = mazes[level_id - 1].strip()
        self.maze = Maze(maze_data)

class Maze:
    def __init__(self, maze_data: str):
        self.tiles = self.parse_maze(maze_data)
        self.level_id = maze_data[0]  # Assuming first character is level id

    def parse_maze(self, maze_data: str):
        return [list(row) for row in maze_data.split(';')]

    def slide_tile(self, direction: str):
        # Logic for sliding tiles based on direction
        pass

    def check_win(self) -> bool:
        # Logic to check if player has reached exit
        return False

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> int:
        return int(time.time() - self.start_time)

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int):
        self.points += points

    def get_score(self) -> int:
        return self.points