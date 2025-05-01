import pygame
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.levels = Levels()
        self.current_level = self.levels.get_next_level()

    def start_game(self):
        self.grid.display()
        # Game loop would go here
        # For now, just simulate clearing blocks and updating score
        self.clear_blocks()
        self.update_score(10)

    def clear_blocks(self):
        # Simulate clearing blocks
        print("Blocks cleared!")

    def update_score(self, points: int):
        self.score.add_points(points)
        print(f"Score updated to: {self.score.get_score()}")

class Grid:
    def __init__(self):
        self.blocks = [[Block(random.choice(['red', 'green', 'blue'])) for _ in range(5)] for _ in range(5)]

    def display(self):
        for row in self.blocks:
            print(" | ".join(block.get_color() for block in row))

    def check_connection(self, start, end):
        # Dummy implementation for checking connection
        return True

class Block:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int):
        self.points += points

    def get_score(self):
        return self.points

class Levels:
    def __init__(self):
        self.level_data = []
        self.load_levels()

    def load_levels(self):
        with open('levels.txt', 'r') as file:
            self.level_data = [line.strip() for line in file.readlines()]

    def get_next_level(self):
        return self.level_data[0] if self.level_data else None