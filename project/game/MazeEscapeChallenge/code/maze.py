import random

class Maze:
    def __init__(self):
        self.walls = []
        self.pathways = []
        self.size = 0
        self.exit_position = (0, 0)

    def load_maze(self, filename: str):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            size, difficulty = line.split('|')
            self.generate_maze(int(size), difficulty)

    def generate_maze(self, size: int, difficulty: str):
        self.size = size
        self.walls = [[1 for _ in range(size)] for _ in range(size)]  # Initialize walls
        self.pathways = [[0 for _ in range(size)] for _ in range(size)]  # Initialize pathways
        self._recursive_backtracking(0, 0)  # Start maze generation
        self.exit_position = (size - 1, size - 1)  # Set exit position

    def _recursive_backtracking(self, x: int, y: int):
        self.pathways[x][y] = 1  # Mark current position as a pathway
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  # Randomize directions for backtracking

        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Calculate next position
            if self.within_bounds(nx, ny) and self.pathways[nx][ny] == 0:  # Ensure position is in bounds and unvisited
                self.walls[x + dx // 2][y + dy // 2] = 0  # Remove the wall between
                self._recursive_backtracking(nx, ny)  # Recursive call for next position

    def within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def display_maze(self):
        for row in self.walls:
            print(' '.join(['#' if cell else ' ' for cell in row]))  # Display the maze