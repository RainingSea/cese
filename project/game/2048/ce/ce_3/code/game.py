import random
from tile import Tile

class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.start_game()

    def start_game(self) -> None:
        self.generate_tile()
        self.generate_tile()

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        elif direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        self.generate_tile()

    def generate_tile(self) -> None:
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = Tile(2 if random.random() < 0.9 else 4)

    def check_game_over(self) -> bool:
        for row in self.board:
            if 0 in row:
                return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j].value == self.board[i + 1][j].value) or \
                   (j < 3 and self.board[i][j].value == self.board[i][j + 1].value):
                    return False
        return True

    def save_game(self, filename: str) -> None:
        with open(filename, 'w') as file:
            flat_board = [str(tile.value) for row in self.board for tile in row]
            file.write(','.join(flat_board) + ',' + str(self.score))

    def load_game(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data = file.read().strip().split(',')
            self.score = int(data[-1])
            for i in range(4):
                for j in range(4):
                    self.board[i][j] = Tile(int(data[i * 4 + j]))