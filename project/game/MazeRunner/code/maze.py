import pygame
import random

class Maze:
    def __init__(self):
        self.layout = []
        self.obstacles = []

    def generate_maze(self, level: int):
        self.layout = [[random.choice([' ', '#']) for _ in range(10)] for _ in range(10)]  # Random layout
        self.obstacles = [(x, y) for y in range(10) for x in range(10) if self.layout[y][x] == '#']  # Populate obstacles

    def check_collision(self, position: tuple) -> bool:
        return position in self.obstacles  # Check for collisions with walls

    def render(self, screen):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == ' ' else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))  # Draw maze cells