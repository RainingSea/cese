import random

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()

    def generate_maze(self) -> list:
        # Simple maze generation algorithm (randomized)
        maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
        for x in range(1, self.width - 1, 2):
            for y in range(1, self.height - 1, 2):
                maze[y][x] = ' '
                if random.choice([True, False]):
                    if x + 1 < self.width - 1:
                        maze[y][x + 1] = ' '
                else:
                    if y + 1 < self.height - 1:
                        maze[y + 1][x] = ' '
        maze[1][0] = ' '  # Entrance
        maze[self.height - 2][self.width - 1] = ' '  # Exit
        return maze

    def display(self) -> None:
        for row in self.grid:
            print(''.join(row))