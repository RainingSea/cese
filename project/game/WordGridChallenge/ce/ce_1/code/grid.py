import random

class Grid:
    def __init__(self):
        self.letters = []
        self.found_words = []

    def generate_grid(self, size: int) -> None:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.letters = [[random.choice(alphabet) for _ in range(size)] for _ in range(size)]

    def display_grid(self) -> None:
        for row in self.letters:
            print(' '.join(row))

    def select_letter(self, x: int, y: int) -> str:
        if 0 <= x < len(self.letters) and 0 <= y < len(self.letters[0]):
            return self.letters[x][y]
        return ''