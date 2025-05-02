import random

class GameBoard:
    def __init__(self):
        self.tiles = []

    def initialize_board(self):
        self.tiles = [[0 for _ in range(4)] for _ in range(4)]
        self.generate_tile()
        self.generate_tile()

    def generate_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.tiles[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.tiles[i][j] = 4 if random.random() < 0.1 else 2

    def move_tiles(self, direction: str):
        if direction == 'up':
            self.move_and_merge_up()
        elif direction == 'down':
            self.move_and_merge_down()
        elif direction == 'left':
            self.move_and_merge_left()
        elif direction == 'right':
            self.move_and_merge_right()

    def move_and_merge_up(self):
        for j in range(4):
            column = [self.tiles[i][j] for i in range(4) if self.tiles[i][j] != 0]
            merged_column = []
            skip = False
            for i in range(len(column)):
                if skip:
                    skip = False
                    continue
                if i < len(column) - 1 and column[i] == column[i + 1]:
                    merged_column.append(column[i] * 2)
                    self.score += column[i] * 2
                    skip = True
                else:
                    merged_column.append(column[i])
            merged_column += [0] * (4 - len(merged_column))
            for i in range(4):
                self.tiles[i][j] = merged_column[i]
        self.generate_tile()

    def move_and_merge_down(self):
        for j in range(4):
            column = [self.tiles[i][j] for i in range(3, -1, -1) if self.tiles[i][j] != 0]
            merged_column = []
            skip = False
            for i in range(len(column)):
                if skip:
                    skip = False
                    continue
                if i < len(column) - 1 and column[i] == column[i + 1]:
                    merged_column.append(column[i] * 2)
                    self.score += column[i] * 2
                    skip = True
                else:
                    merged_column.append(column[i])
            merged_column += [0] * (4 - len(merged_column))
            for i in range(4):
                self.tiles[3 - i][j] = merged_column[i]
        self.generate_tile()

    def move_and_merge_left(self):
        for i in range(4):
            row = [self.tiles[i][j] for j in range(4) if self.tiles[i][j] != 0]
            merged_row = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    merged_row.append(row[j] * 2)
                    self.score += row[j] * 2
                    skip = True
                else:
                    merged_row.append(row[j])
            merged_row += [0] * (4 - len(merged_row))
            for j in range(4):
                self.tiles[i][j] = merged_row[j]
        self.generate_tile()

    def move_and_merge_right(self):
        for i in range(4):
            row = [self.tiles[i][j] for j in range(3, -1, -1) if self.tiles[i][j] != 0]
            merged_row = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    merged_row.append(row[j] * 2)
                    self.score += row[j] * 2
                    skip = True
                else:
                    merged_row.append(row[j])
            merged_row += [0] * (4 - len(merged_row))
            for j in range(4):
                self.tiles[i][3 - j] = merged_row[j]
        self.generate_tile()

    def check_game_over(self):
        if any(0 in row for row in self.tiles):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.tiles[i][j] == self.tiles[i + 1][j]) or \
                   (j < 3 and self.tiles[i][j] == self.tiles[i][j + 1]):
                    return False
        return True

    def save_game(self):
        with open('game_state.txt', 'w') as file:
            for row in self.tiles:
                file.write(','.join(map(str, row)) + '\n')
            file.write(str(self.score) + '\n')

    def load_game(self):
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.tiles = [list(map(int, line.strip().split(','))) for line in lines[:-1]]
            self.score = int(lines[-1].strip())
            
class Game:
    def __init__(self):
        self.board = GameBoard()
        self.score = 0

    def start_game(self):
        self.board.initialize_board()
        # Main game loop would go here

    def move(self, direction: str):
        self.board.move_tiles(direction)

    def check_game_over(self):
        return self.board.check_game_over()

    def save_game(self):
        self.board.save_game()

    def load_game(self):
        self.board.load_game()