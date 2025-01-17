import random

class Tile:
    def __init__(self, value: int):
        self.value = value

class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.start_game()

    def start_game(self):
        self.generate_tile()
        self.generate_tile()

    def generate_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = random.choice([2, 4])

    def move(self, direction: str) -> bool:
        moved = False
        if direction == 'up':
            for j in range(4):
                column = [self.board[i][j] for i in range(4)]
                new_column, col_moved = self.merge(column)
                for i in range(4):
                    if new_column[i] != self.board[i][j]:
                        moved = True
                    self.board[i][j] = new_column[i]
                if col_moved:
                    self.generate_tile()
        elif direction == 'down':
            for j in range(4):
                column = [self.board[i][j] for i in range(3, -1, -1)]
                new_column, col_moved = self.merge(column)
                for i in range(4):
                    if new_column[i] != self.board[3 - i][j]:
                        moved = True
                    self.board[3 - i][j] = new_column[i]
                if col_moved:
                    self.generate_tile()
        elif direction == 'left':
            for i in range(4):
                row = self.board[i]
                new_row, row_moved = self.merge(row)
                for j in range(4):
                    if new_row[j] != self.board[i][j]:
                        moved = True
                    self.board[i][j] = new_row[j]
                if row_moved:
                    self.generate_tile()
        elif direction == 'right':
            for i in range(4):
                row = self.board[i][::-1]
                new_row, row_moved = self.merge(row)
                for j in range(4):
                    if new_row[j] != self.board[i][3 - j]:
                        moved = True
                    self.board[i][3 - j] = new_row[j]
                if row_moved:
                    self.generate_tile()
        return moved

    def merge(self, line):
        new_line = [value for value in line if value != 0]
        moved = False
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1] and new_line[i] != 0:
                new_line[i] *= 2
                self.score += new_line[i]
                new_line[i + 1] = 0
                moved = True
        new_line = [value for value in new_line if value != 0]
        new_line += [0] * (4 - len(new_line))
        return new_line, moved

    def check_game_over(self) -> bool:
        for row in self.board:
            if 0 in row:
                return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def save_game(self, file_name: str):
        with open(file_name, 'w') as f:
            f.write(f'score: {self.score}\n')
            for row in self.board:
                f.write(','.join(map(str, row)) + '\n')

    def load_game(self, file_name: str):
        with open(file_name, 'r') as f:
            lines = f.readlines()
            self.score = int(lines[0].strip().split(': ')[1])
            for i in range(4):
                self.board[i] = list(map(int, lines[i + 1].strip().split(',')))