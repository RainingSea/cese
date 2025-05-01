import pygame
import random

class Grid:
    def __init__(self) -> None:
        self.blocks = self.generate_initial_blocks()

    def generate_initial_blocks(self) -> list:
        return [['empty' for _ in range(10)] for _ in range(10)]

    def display(self) -> None:
        for y, row in enumerate(self.blocks):
            for x, color in enumerate(row):
                pygame.draw.rect(pygame.display.get_surface(), self.get_color(color), (x * 50, y * 50, 50, 50))

    def get_color(self, color: str) -> tuple:
        color_map = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'empty': (255, 255, 255)
        }
        return color_map.get(color, (255, 255, 255))

    def fall_blocks(self) -> None:
        for x in range(10):
            empty_space = 0
            for y in range(9, -1, -1):
                if self.blocks[y][x] == 'empty':
                    empty_space += 1
                elif empty_space > 0:
                    self.blocks[y + empty_space][x] = self.blocks[y][x]
                    self.blocks[y][x] = 'empty'

    def generate_new_blocks(self) -> None:
        for x in range(10):
            for y in range(10):
                if self.blocks[y][x] == 'empty':
                    self.blocks[y][x] = random.choice(['red', 'green', 'blue', 'yellow'])

    def get_selected_blocks(self, x: int, y: int) -> list:
        return [(x, y)] if self.blocks[y][x] != 'empty' else []

    def connect_blocks(self, x: int, y: int) -> list:
        color = self.blocks[y][x]
        connected_blocks = []
        self._find_connected_blocks(x, y, color, connected_blocks)
        return connected_blocks

    def _find_connected_blocks(self, x: int, y: int, color: str, connected_blocks: list) -> None:
        if x < 0 or x >= 10 or y < 0 or y >= 10 or self.blocks[y][x] != color or (x, y) in connected_blocks:
            return
        connected_blocks.append((x, y))
        self._find_connected_blocks(x + 1, y, color, connected_blocks)
        self._find_connected_blocks(x - 1, y, color, connected_blocks)
        self._find_connected_blocks(x, y + 1, color, connected_blocks)
        self._find_connected_blocks(x, y - 1, color, connected_blocks)

    def clear_blocks(self, selected_blocks) -> None:
        for x, y in selected_blocks:
            self.blocks[y][x] = 'empty'

    def restore_blocks(self, last_move) -> None:
        for x, y in last_move:
            self.blocks[y][x] = random.choice(['red', 'green', 'blue', 'yellow'])

    def load_from_data(self, lines: list) -> None:
        self.blocks = [line.strip().split('|') for line in lines]

    def save_to_data(self) -> str:
        return '\n'.join(['|'.join(row) for row in self.blocks])