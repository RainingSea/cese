import random

class Game:
    def __init__(self):
        self.grid = self.create_grid()
        self.score = 0
        self.level = 1

    def create_grid(self) -> list[list[str]]:
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        return [[random.choice(colors) for _ in range(8)] for _ in range(8)]

    def start_game(self) -> None:
        self.grid = self.create_grid()
        self.score = 0
        self.level = 1

    def draw_grid(self) -> None:
        # Placeholder for drawing the grid logic
        pass

    def connect_blocks(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        # Placeholder for connection logic
        pass

    def clear_blocks(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        # Placeholder for clearing blocks logic
        pass

    def update_score(self, points: int) -> None:
        self.score += points

    def next_level(self) -> None:
        self.level += 1
        self.start_game()