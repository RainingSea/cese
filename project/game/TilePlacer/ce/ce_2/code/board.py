from typing import List, Tuple
from tile import Tile

class Board:
    def __init__(self):
        self.grid: List[List[Tile]] = [[None for _ in range(8)] for _ in range(8)]  # 8x8 grid

    def display_board(self):
        for row in self.grid:
            print(' | '.join(tile.color if tile else 'Empty' for tile in row))

    def update_tile(self, position: Tuple[int, int], tile: Tile):
        x, y = position
        self.grid[x][y] = tile