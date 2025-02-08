from typing import List, Tuple
from gem import Gem

class GameBoard:
    def __init__(self, rows: int, cols: int):
        self.grid: List[List[Gem]] = [[Gem("red") for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.level = 1
        self.timer = 60  # seconds

    def swap_gems(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        # Swap the gems at the given positions
        self.grid[pos1[0]][pos1[1]], self.grid[pos2[0]][pos2[1]] = self.grid[pos2[0]][pos2[1]], self.grid[pos1[0]][pos1[1]]
        return True  # Simplified for now

    def check_matches(self) -> List[List[Tuple[int, int]]]:
        # Placeholder for match checking logic
        return []

    def clear_matches(self, matches: List[List[Tuple[int, int]]]):
        # Placeholder for clearing matched gems
        pass

    def fall_gems(self):
        # Placeholder for falling gems logic
        pass

    def update_score(self, points: int):
        self.score += points

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.timer = 60
        self.grid = [[Gem("red") for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]