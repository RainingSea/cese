import random

class Maze:
    def __init__(self):
        self.walls = []
        self.pathways = []
        self.size = 0

    def generate_maze(self, size: int):
        self.size = size
        self.walls = [[1 for _ in range(size)] for _ in range(size)]
        self.pathways = [[0 for _ in range(size)] for _ in range(size)]
        self._recursive_backtracking(0, 0)

    def _recursive_backtracking(self, x: int, y: int):
        self.pathways[x][y] = 1
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.pathways[nx][ny] == 0:
                self.walls[x + dx // 2][y + dy // 2] = 0
                self._recursive_backtracking(nx, ny)

    def display_maze(self):
        for row in self.walls:
            print(' '.join(['#' if cell else ' ' for cell in row]))