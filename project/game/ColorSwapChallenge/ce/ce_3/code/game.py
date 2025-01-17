import random
import json

class Block:
    def __init__(self, color: str):
        self.color = color

class Grid:
    def __init__(self):
        self.blocks = []

    def initialize_grid(self, size: tuple) -> None:
        self.blocks = [[Block(random.choice(['red', 'green', 'blue', 'yellow', 'purple'])) for _ in range(size[1])] for _ in range(size[0])]

    def get_block(self, pos: tuple) -> Block:
        return self.blocks[pos[0]][pos[1]]

    def set_block(self, pos: tuple, block: Block) -> None:
        self.blocks[pos[0]][pos[1]] = block

class Score:
    def __init__(self):
        self.total_score = 0

    def add_points(self, points: int) -> None:
        self.total_score += points

    def get_score(self) -> int:
        return self.total_score

class Level:
    def __init__(self, level_number: int, grid_size: tuple):
        self.level_number = level_number
        self.grid_size = grid_size

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.level = None
        self.moves_left = 0

    def start_game(self) -> None:
        self.load_level(1)

    def swap_blocks(self, pos1: tuple, pos2: tuple) -> bool:
        block1 = self.grid.get_block(pos1)
        block2 = self.grid.get_block(pos2)
        if block1 and block2:
            self.grid.set_block(pos1, block2)
            self.grid.set_block(pos2, block1)
            return True
        return False

    def check_matches(self) -> list:
        matches = []
        # Logic to check for matches (not implemented here)
        return matches

    def clear_matches(self, matches: list) -> None:
        for match in matches:
            self.grid.set_block(match, Block(random.choice(['red', 'green', 'blue', 'yellow', 'purple'])))
        self.update_score(len(matches) * 10)

    def update_score(self, points: int) -> None:
        self.score.add_points(points)

    def load_level(self, level_number: int) -> None:
        with open('levels.txt', 'r') as file:
            levels = json.load(file)
            level_info = levels[str(level_number)]
            self.level = Level(level_number, tuple(level_info['grid_size']))
            self.grid.initialize_grid(self.level.grid_size)
            self.moves_left = level_info['moves']

    def save_game(self) -> None:
        game_data = {
            'level': self.level.level_number,
            'score': self.score.get_score(),
            'moves_left': self.moves_left
        }
        with open('game_data.txt', 'w') as file:
            json.dump(game_data, file)

    def load_game(self) -> None:
        with open('game_data.txt', 'r') as file:
            game_data = json.load(file)
            self.level = Level(game_data['level'], (0, 0))  # Load level size later
            self.score.total_score = game_data['score']
            self.moves_left = game_data['moves_left']
            self.load_level(self.level.level_number)