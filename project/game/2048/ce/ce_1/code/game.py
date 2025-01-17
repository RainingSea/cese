import random

class Game:
    def __init__(self) -> None:
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.generate_tile()
        self.generate_tile()

    def start_game(self) -> None:
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.generate_tile()
        self.generate_tile()

    def move(self, direction: str) -> None:
        if direction == 'up':
            self._move_up()
        elif direction == 'down':
            self._move_down()
        elif direction == 'left':
            self._move_left()
        elif direction == 'right':
            self._move_right()
        self.generate_tile()

    def generate_tile(self) -> None:
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def check_game_over(self) -> bool:
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def save_game_state(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(f"{self.score}\n")
            for row in self.board:
                f.write(' '.join(map(str, row)) + '\n')

    def load_game_state(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self.score = int(f.readline().strip())
            for i in range(4):
                self.board[i] = list(map(int, f.readline().strip().split()))

    def _move_up(self) -> None:
        for j in range(4):
            column = [self.board[i][j] for i in range(4)]
            new_column = self._merge(column)
            for i in range(4):
                self.board[i][j] = new_column[i]

    def _move_down(self) -> None:
        for j in range(4):
            column = [self.board[i][j] for i in range(4)][::-1]
            new_column = self._merge(column)
            for i in range(4):
                self.board[i][j] = new_column[::-1][i]

    def _move_left(self) -> None:
        for i in range(4):
            new_row = self._merge(self.board[i])
            self.board[i] = new_row

    def _move_right(self) -> None:
        for i in range(4):
            new_row = self._merge(self.board[i][::-1])
            self.board[i] = new_row[::-1]

    def _merge(self, line: list) -> list:
        new_line = [num for num in line if num != 0]
        merged_line = []
        skip = False
        for i in range(len(new_line)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
                merged_line.append(new_line[i] * 2)
                self.score += new_line[i] * 2
                skip = True
            else:
                merged_line.append(new_line[i])
        merged_line += [0] * (4 - len(merged_line))
        return merged_line