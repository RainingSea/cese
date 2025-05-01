import pygame
import time
import random

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time

class Player:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, direction):
        if direction == 'UP':
            self.position[1] -= 1
        elif direction == 'DOWN':
            self.position[1] += 1
        elif direction == 'LEFT':
            self.position[0] -= 1
        elif direction == 'RIGHT':
            self.position[0] += 1

    def check_exit(self, exit_position):
        return self.position == exit_position

class Maze:
    def __init__(self):
        self.grid = []

    def generate_maze(self, size, difficulty):
        self.grid = [['#' for _ in range(size)] for _ in range(size)]
        # Simple maze generation logic for demo purposes
        for i in range(size):
            for j in range(size):
                if random.random() > difficulty:
                    self.grid[i][j] = ' '

    def display_maze(self):
        for row in self.grid:
            print(''.join(row))

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player([1, 1])
        self.timer = Timer()
        self.exit_position = [5, 5]  # Example exit position

    def start_game(self):
        self.maze.generate_maze(10, 0.3)
        self.timer.start()
        self.play()

    def restart_level(self):
        self.player.position = [1, 1]
        self.start_game()

    def display_feedback(self):
        print("Congratulations! You've reached the exit!")

    def play(self):
        running = True
        while running:
            self.maze.display_maze()
            print(f"Player Position: {self.player.position}")
            print("Use arrow keys to move (UP, DOWN, LEFT, RIGHT) or type 'exit' to quit:")
            command = input().strip().upper()
            if command == 'EXIT':
                running = False
            else:
                self.player.move(command)
                if self.player.check_exit(self.exit_position):
                    self.timer.stop()
                    self.display_feedback()
                    running = False