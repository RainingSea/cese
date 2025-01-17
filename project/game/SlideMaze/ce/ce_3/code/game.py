import pygame
from maze import Maze
from player import Player
from timer import Timer

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()
        self.score = 0

    def start_game(self):
        self.load_maze(1)
        self.timer.start()
        self.game_loop()

    def reset_maze(self):
        self.load_maze(1)

    def load_maze(self, level: int):
        layout = self.read_maze_from_file(level)
        self.maze.initialize_maze(layout)

    def read_maze_from_file(self, level: int) -> str:
        with open('mazes.txt', 'r') as file:
            mazes = file.read().strip().split('\n')
            return mazes[level - 1]  # level is 1-indexed

    def update_score(self, points: int):
        self.score += points

    def game_loop(self):
        # Placeholder for the game loop logic
        pass