import pygame

class Grid:
    def __init__(self):
        self.cells = [[0 for _ in range(9)] for _ in range(9)]

    def display(self):
        # Code to display the grid using Pygame
        for row in range(9):
            for col in range(9):
                cell_value = self.cells[row][col]
                # Render cell_value using Pygame
                # Placeholder for rendering logic
                pass

    def update_cell(self, row: int, col: int, symbol: str) -> bool:
        if self.check_validity(row, col, symbol) and self.cells[row][col] == 0:
            self.cells[row][col] = int(symbol)  # Ensure symbol is stored as an integer
            return True
        return False

    def check_validity(self, row: int, col: int, symbol: str) -> bool:
        return self.validate() and self.check_row(row, symbol) and self.check_column(col, symbol) and self.check_subgrid(row, col, symbol)

    def check_row(self, row: int, symbol: str) -> bool:
        return symbol not in [str(num) for num in self.cells[row] if num != 0]

    def check_column(self, col: int, symbol: str) -> bool:
        return symbol not in [str(self.cells[row][col]) for row in range(9) if self.cells[row][col] != 0]

    def check_subgrid(self, row: int, col: int, symbol: str) -> bool:
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for r in range(subgrid_row_start, subgrid_row_start + 3):
            for c in range(subgrid_col_start, subgrid_col_start + 3):
                if self.cells[r][c] == int(symbol):
                    return False
        return True

    def validate(self) -> bool:
        for row in self.cells:
            if len(set(row)) != len([cell for cell in row if cell != 0]):
                return False
        for col in range(9):
            if len(set(self.cells[row][col] for row in range(9))) != len([self.cells[row][col] for row in range(9) if self.cells[row][col] != 0]):
                return False
        return True

    def load(self, puzzle):
        for i, row in enumerate(puzzle):
            self.cells[i] = row

    def clear(self):
        self.cells = [[0 for _ in range(9)] for _ in range(9)]

    def is_full(self) -> bool:
        return all(cell != 0 for row in self.cells for cell in row)