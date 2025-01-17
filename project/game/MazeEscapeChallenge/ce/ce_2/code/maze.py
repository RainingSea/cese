import random

class Maze:
    def __init__(self):
        self.grid = []
        self.size = 0

    def generate(self, size: int) -> None:
        self.size = size
        self.grid = [['#' for _ in range(size)] for _ in range(size)]
        self._recursive_backtracking(0, 0)

    def _recursive_backtracking(self, x: int, y: int) -> None:
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == '#':
                self.grid[y + dy // 2][x + dx // 2] = ' '
                self.grid[ny][nx] = ' '
                self._recursive_backtracking(nx, ny)

    def render(self, screen) -> None:
        for y in range(self.size):
            for x in range(self.size):
                color = (255, 255, 255) if self.grid[y][x] == ' ' else (0, 0, 0)
                screen.fill(color, rect=(x * 20, y * 20, 20, 20))

    def is_exit_reached(self, player_pos: tuple) -> bool:
        return player_pos == (self.size - 1, self.size - 1)