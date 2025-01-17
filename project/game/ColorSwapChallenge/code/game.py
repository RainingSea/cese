import pygame
import random
import os

class Block:
    def __init__(self, color: str) -> None:
        self.color = color

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size
        self.blocks = []
        self.create_grid(size)

    def create_grid(self, size: int) -> None:
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        self.blocks = [[Block(random.choice(colors)) for _ in range(size)] for _ in range(size)]

    def get_adjacent_blocks(self, pos: tuple) -> list:
        x, y = pos
        adjacent = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                adjacent.append(self.blocks[x + dx][y + dy])
        return adjacent

    def check_matches(self) -> list:
        matches = []
        for x in range(self.size):
            for y in range(self.size):
                block = self.blocks[x][y]
                # Check horizontal matches
                if y <= self.size - 3 and block.color == self.blocks[x][y + 1].color == self.blocks[x][y + 2].color:
                    matches.append([(x, y), (x, y + 1), (x, y + 2)])
                # Check vertical matches
                if x <= self.size - 3 and block.color == self.blocks[x + 1][y].color == self.blocks[x + 2][y].color:
                    matches.append([(x, y), (x + 1, y), (x + 2, y)])
        return matches

    def clear_matches(self, matches: list) -> None:
        for match in matches:
            for x, y in match:
                self.blocks[x][y] = Block(random.choice(['red', 'green', 'blue', 'yellow', 'purple']))

    def update_grid(self) -> None:
        # Logic to update the grid after matches are cleared
        for x in range(self.size):
            for y in range(self.size):
                if self.blocks[x][y].color == '':
                    self.blocks[x][y] = Block(random.choice(['red', 'green', 'blue', 'yellow', 'purple']))

class Score:
    def __init__(self) -> None:
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

    def reset_score(self) -> None:
        self.points = 0

class Level:
    def __init__(self) -> None:
        self.current_level = 1
        self.move_limit = 0
        self.grid = []

    def load_level(self, level_number: int) -> None:
        self.current_level = level_number
        level_file = f'level_{level_number}.txt'
        if os.path.exists(level_file):
            with open(level_file, 'r') as file:
                data = file.readlines()
                self.move_limit = int(data[0].strip())
                # Load grid configuration
                grid_data = data[1].strip().split('|')
                self.grid = [grid_data[i:i + 8] for i in range(0, len(grid_data), 8)]

    def next_level(self) -> None:
        self.current_level += 1
        self.load_level(self.current_level)

    def get_level(self) -> int:
        return self.current_level

class PowerUp:
    def __init__(self, type: str) -> None:
        self.type = type

    def activate(self, grid: Grid) -> None:
        if self.type == 'extra_move':
            # Logic to add an extra move
            pass
        elif self.type == 'color_bomb':
            # Logic to clear all blocks of a certain color
            pass
        elif self.type == 'shuffle':
            # Logic to shuffle the grid
            random.shuffle(grid.blocks)

class MoveCounter:
    def __init__(self, moves_left: int) -> None:
        self.moves_left = moves_left

    def decrement(self) -> None:
        self.moves_left -= 1

    def get_moves(self) -> int:
        return self.moves_left

class Game:
    def __init__(self) -> None:
        self.grid = Grid(size=8)
        self.score = Score()
        self.level = Level()
        self.moves_used = 0
        self.move_counter = MoveCounter(moves_left=self.level.move_limit)

    def start_game(self) -> None:
        self.level.load_level(1)
        self.move_counter = MoveCounter(moves_left=self.level.move_limit)
        while self.move_counter.get_moves() > 0:
            matches = self.grid.check_matches()
            if matches:
                self.grid.clear_matches(matches)
                self.update_score(len(matches))
                self.grid.update_grid()  # Update grid after clearing matches
            else:
                # Logic for player input and rendering would go here
                pass
            self.move_counter.decrement()
            self.moves_used += 1  # Track moves used
            if self.move_counter.get_moves() == 0:
                self.level.next_level()  # Move to the next level if moves are exhausted

    def swap_blocks(self, pos1: tuple, pos2: tuple) -> bool:
        # Logic to swap blocks and check if the swap is valid
        return True

    def update_score(self, matches_count: int) -> None:
        points = matches_count * 10  # Example scoring logic
        self.score.add_points(points)

    def load_game_data(self) -> None:
        if os.path.exists('game_data.txt'):
            with open('game_data.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    key, value = line.strip().split('|')
                    if key == 'score':
                        self.score.points = int(value)
                    elif key == 'level':
                        self.level.current_level = int(value)
                        self.level.load_level(self.level.current_level)  # Load the level data
                    elif key == 'moves_used':
                        self.moves_used = int(value)

    def save_game_data(self) -> None:
        with open('game_data.txt', 'w') as file:
            file.write(f'score|{self.score.points}\n')
            file.write(f'level|{self.level.current_level}\n')
            file.write(f'moves_used|{self.moves_used}\n')