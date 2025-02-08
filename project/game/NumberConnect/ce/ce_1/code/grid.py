import random

class Grid:
    def __init__(self):
        self.tiles = []

    def generate_grid(self, level: int) -> None:
        """Generates a grid of numbered tiles based on the difficulty level."""
        size = level + 2  # Example: level 1 -> 3x3 grid
        self.tiles = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]

    def get_tile(self, x: int, y: int) -> int:
        """Returns the value of the tile at the specified coordinates."""
        return self.tiles[y][x]