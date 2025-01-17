import json
import random

class Tile:
    def __init__(self, value: int):
        self.value = value

    def merge(self, other: 'Tile') -> bool:
        if self.value == other.value:
            self.value *= 2
            return True
        return False


class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.generate_tile()
        self.generate_tile()

    def start_game(self):
        while not self.game_over:
            self.display_board()
            direction = input("Enter move (w/a/s/d): ")
            if not self.move(direction):
                print("Invalid move! Try again.")
            self.check_game_over()

    def move(self, direction: str) -> bool:
        moved = False
        if direction in ['w', 'a', 's', 'd']:
            # Implement movement logic
            if direction == 'w':
                for col in range(4):
                    merged_row = []
                    for row in range(4):
                        if self.board[row][col] != 0:
                            merged_row.append(Tile(self.board[row][col]))
                    merged_row = self.merge_tiles(merged_row)
                    for row in range(4):
                        self.board[row][col] = merged_row[row].value if row < len(merged_row) else 0
                    moved = True

            # Similar logic for 'a', 's', 'd' can be implemented here

            if moved:
                self.generate_tile()
                return True
        return False

    def merge_tiles(self, tiles: list) -> list:
        merged = []
        skip = False
        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            if i + 1 < len(tiles) and tiles[i].merge(tiles[i + 1]):
                self.score += tiles[i].value
                skip = True
            merged.append(tiles[i])
        return merged

    def generate_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def check_game_over(self):
        if all(self.board[r][c] != 0 for r in range(4) for c in range(4)):
            self.game_over = True

    def save_game(self, filename: str):
        with open(filename, 'w') as f:
            json.dump({'board': self.board, 'score': self.score}, f)

    def load_game(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.board = data['board']
            self.score = data['score']

    def display_board(self):
        for row in self.board:
            print("\t".join(str(tile) if tile != 0 else '.' for tile in row))
        print(f"Score: {self.score}")