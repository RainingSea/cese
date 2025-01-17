import random
from tile import Tile

class Board:
    def __init__(self):
        self.tiles = [[0] * 4 for _ in range(4)]
        self.initialize()

    def initialize(self) -> None:
        for _ in range(2):
            self.add_random_tile()

    def add_random_tile(self) -> None:
        empty_cells = self.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.tiles[row][col] = Tile(2 if random.random() < 0.9 else 4)

    def move(self, direction: str) -> bool:
        if direction in ['up', 'down', 'left', 'right']:
            moved = self.merge_tiles(direction)
            if moved:
                self.add_random_tile()
            return moved
        return False

    def merge_tiles(self, direction: str) -> bool:
        moved = False
        if direction == 'left':
            for row in self.tiles:
                moved |= self._merge_row(row)
        elif direction == 'right':
            for row in self.tiles:
                moved |= self._merge_row(row[::-1])
                row.reverse()
        elif direction == 'up':
            for col in range(4):
                moved |= self._merge_column(col)
        elif direction == 'down':
            for col in range(4):
                moved |= self._merge_column(col, reverse=True)
        return moved

    def _merge_row(self, row: list) -> bool:
        moved = False
        new_row = [tile.get_value() for tile in row if tile != 0]
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                del new_row[i + 1]
                moved = True
            i += 1
        new_row += [0] * (4 - len(new_row))
        for j in range(4):
            if row[j] != new_row[j]:
                moved = True
            row[j] = Tile(new_row[j]) if new_row[j] != 0 else 0
        return moved

    def _merge_column(self, col: int, reverse: bool = False) -> bool:
        moved = False
        column = [self.tiles[row][col] for row in range(4)]
        if reverse:
            column = column[::-1]
        moved |= self._merge_row(column)
        if reverse:
            column.reverse()
        for row in range(4):
            self.tiles[row][col] = column[row]
        return moved

    def get_empty_cells(self) -> list:
        return [(i, j) for i in range(4) for j in range(4) if self.tiles[i][j] == 0]

    def to_dict(self) -> dict:
        return {
            'tiles': [[tile.get_value() if tile != 0 else 0 for tile in row] for row in self.tiles]
        }