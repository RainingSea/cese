import random

class Maze:
    def __init__(self):
        self.layout = []
        self.obstacles = []

    def generate_maze(self):
        # Simple maze generation logic
        self.layout = [[random.choice([' ', '#']) for _ in range(10)] for _ in range(10)]
        self.obstacles = [(x, y) for x in range(10) for y in range(10) if self.layout[x][y] == '#']

    def display(self):
        # Placeholder for display logic
        pass