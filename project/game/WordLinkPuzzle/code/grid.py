import random
import pygame

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, difficulty: str):
        size = self.get_grid_size(difficulty)
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def get_grid_size(self, difficulty: str) -> int:
        if difficulty == 'Easy':
            return 4
        elif difficulty == 'Medium':
            return 6
        elif difficulty == 'Hard':
            return 8
        return 4  # Default to Easy

    def display_grid(self, screen):
        font = pygame.font.Font(None, 36)
        for row_index, row in enumerate(self.letters):
            for col_index, letter in enumerate(row):
                text = font.render(letter, True, (0, 0, 0))
                screen.blit(text, (col_index * 50 + 100, row_index * 50 + 100))  # Adjust position as needed

    def connect_letters(self, start: tuple, end: tuple) -> list:
        letters_connected = []
        row_start, col_start = start
        row_end, col_end = end
        
        if row_start == row_end:  # Horizontal connection
            for col in range(col_start, col_end + 1):
                letters_connected.append(self.letters[row_start][col])
        elif col_start == col_end:  # Vertical connection
            for row in range(row_start, row_end + 1):
                letters_connected.append(self.letters[row][col_start])
        else:  # Diagonal connection (not implemented for simplicity)
            pass
        
        return letters_connected