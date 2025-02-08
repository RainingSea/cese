import pygame
import random
import time

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def get_time(self):
        return time.time() - self.start_time


class Player:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, direction):
        if direction == 'up':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'down':
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == 'left':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 1, self.position[1])

    def get_position(self):
        return self.position


class Maze:
    def __init__(self):
        self.grid = []
        self.size = (0, 0)

    def generate_maze(self, size):
        self.size = size
        self.grid = [['#' for _ in range(size[0])] for _ in range(size[1])]
        self._create_path(1, 1)

    def _create_path(self, x, y):
        self.grid[y][x] = ' '
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.size[0] and 0 < ny < self.size[1] and self.grid[ny][nx] == '#':
                self.grid[y + dy // 2][x + dx // 2] = ' '
                self._create_path(nx, ny)

    def display(self):
        for row in self.grid:
            print(''.join(row))

    def is_exit(self, position):
        return position == (self.size[0] - 2, self.size[1] - 1)


class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player((1, 1))
        self.timer = Timer()

    def start_game(self):
        self.maze.generate_maze((21, 21))
        self.timer.start()
        self.display_maze()
        self.handle_input()

    def display_maze(self):
        self.maze.display()
        print(f"Player position: {self.player.get_position()}")

    def handle_input(self):
        while True:
            command = input("Enter move (up, down, left, right) or 'exit': ")
            if command == 'exit':
                break
            self.player.move(command)
            if self.maze.is_exit(self.player.get_position()):
                print("You've escaped the maze!")
                print(f"Time taken: {self.timer.get_time()} seconds")
                break
            self.display_maze()

    def check_exit(self):
        return self.maze.is_exit(self.player.get_position())

    def restart_level(self):
        self.start_game()