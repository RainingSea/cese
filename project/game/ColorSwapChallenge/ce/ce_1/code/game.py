import random

class Block:
    def __init__(self, color: str) -> None:
        self.color = color

class Grid:
    def __init__(self):
        self.blocks = []

    def initialize_grid(self, size: int, colors: list) -> None:
        self.blocks = [[Block(random.choice(colors)) for _ in range(size)] for _ in range(size)]

    def get_block(self, pos: tuple) -> Block:
        x, y = pos
        return self.blocks[y][x]

    def set_block(self, pos: tuple, block: Block) -> None:
        x, y = pos
        self.blocks[y][x] = block

class Score:
    def __init__(self) -> None:
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

class Level:
    def __init__(self) -> None:
        self.level_number = 0
        self.move_limit = 0

    def load_level(self, level_number: int) -> None:
        self.level_number = level_number
        # For simplicity, we set a static move limit
        self.move_limit = 20

    def get_move_limit(self) -> int:
        return self.move_limit

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.level = Level()

    def start_game(self) -> None:
        self.level.load_level(1)
        self.grid.initialize_grid(5, ['red', 'green', 'blue', 'yellow', 'purple'])

    def swap_blocks(self, pos1: tuple, pos2: tuple) -> bool:
        block1 = self.grid.get_block(pos1)
        block2 = self.grid.get_block(pos2)
        if self.is_adjacent(pos1, pos2):
            self.grid.set_block(pos1, block2)
            self.grid.set_block(pos2, block1)
            return True
        return False

    def is_adjacent(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)

    def check_matches(self) -> list:
        # Placeholder for match checking logic
        return []

    def clear_matches(self, matches: list) -> None:
        for match in matches:
            for pos in match:
                self.grid.set_block(pos, Block(random.choice(['red', 'green', 'blue', 'yellow', 'purple'])))

    def update_score(self, points: int) -> None:
        self.score.add_points(points)