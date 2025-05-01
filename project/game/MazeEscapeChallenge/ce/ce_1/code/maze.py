import random

class Maze:
    def __init__(self):
        self.grid = []

    def generate_maze(self, size: int, difficulty: str):
        self.grid = [['#' for _ in range(size)] for _ in range(size)]
        # Simple maze generation logic for demonstration
        for i in range(size):
            for j in range(size):
                if random.random() > 0.3:
                    self.grid[i][j] = ' '  # Open path

        # Set entrance and exit
        self.grid[0][1] = ' '
        self.grid[size - 1][size - 2] = ' '

    def display_maze(self):
        for row in self.grid:
            print(''.join(row))