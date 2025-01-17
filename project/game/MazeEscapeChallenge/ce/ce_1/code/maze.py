import random

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()

    def generate_maze(self) -> list:
        maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
        for i in range(1, self.height - 1, 2):
            for j in range(1, self.width - 1, 2):
                maze[i][j] = ' '
                if random.choice([True, False]):
                    if i + 1 < self.height - 1:
                        maze[i + 1][j] = ' '
                else:
                    if j + 1 < self.width - 1:
                        maze[i][j + 1] = ' '
        return maze

    def display_maze(self) -> None:
        for row in self.grid:
            print(''.join(row))