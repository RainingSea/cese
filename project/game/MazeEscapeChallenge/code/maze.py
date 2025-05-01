import random

class Maze:
    def __init__(self):
        self.layout = []

    def generate_maze(self, size: int, difficulty: float):
        self.layout = [[1 for _ in range(size)] for _ in range(size)]
        self._recursive_backtracking(1, 1)

    def _recursive_backtracking(self, x: int, y: int):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < len(self.layout) and 0 < ny < len(self.layout) and self.layout[ny][nx] == 1:
                self.layout[y + dy // 2][x + dx // 2] = 0
                self.layout[ny][nx] = 0
                self._recursive_backtracking(nx, ny)

    def render(self):
        for row in self.layout:
            print(' '.join(['#' if cell == 1 else ' ' for cell in row]))