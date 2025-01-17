import pygame

class Maze:
    def __init__(self):
        self.layout = []
        self.obstacles = []

    def generate_maze(self, level: int) -> None:
        # Logic to generate maze based on level
        pass

    def is_path(self, position: tuple[int, int]) -> bool:
        x, y = position
        return self.layout[y][x] == 0

    def draw(self, screen) -> None:
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))