import random

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int):
        """Generates a grid of letters of given size."""
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def display_grid(self):
        """Displays the current grid of letters."""
        for row in self.letters:
            print(' '.join(row))

    def connect_letters(self, start: tuple, end: tuple) -> list:
        """Connects letters from start to end coordinates and returns the letters."""
        connected_letters = []
        start_row, start_col = start
        end_row, end_col = end

        # Determine the direction of connection
        row_step = (end_row - start_row) // max(1, abs(end_row - start_row))
        col_step = (end_col - start_col) // max(1, abs(end_col - start_col))

        current_row, current_col = start_row, start_col
        while (current_row, current_col) != (end_row, end_col):
            connected_letters.append(self.letters[current_row][current_col])
            current_row += row_step
            current_col += col_step

        connected_letters.append(self.letters[end_row][end_col])  # Add the end letter
        return connected_letters