import random

class Tile:
    def __init__(self, value: int):
        self.value = value

    def draw(self):
        # Placeholder for drawing the tile, to be implemented with Pygame
        pass

class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()

    def start_game(self) -> None:
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()

    def move(self, direction: str) -> None:
        if direction in ['up', 'down', 'left', 'right']:
            # Implement movement logic
            pass

    def spawn_tile(self) -> None:
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = Tile(2 if random.random() < 0.9 else 4)

    def check_game_over(self) -> bool:
        if any(0 in row for row in self.board):
            return False
        # Check for possible merges
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or \
                   (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        self.game_over = True
        return True

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.score}\n")
            for row in self.board:
                f.write('|'.join(str(tile.value) if tile != 0 else '0' for tile in row) + '\n')

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                self.score = int(f.readline().strip())
                for i, line in enumerate(f):
                    values = list(map(int, line.strip().split('|')))
                    self.board[i] = [Tile(value) if value != 0 else 0 for value in values]
        except FileNotFoundError:
            print("No saved game state found.")

    def draw_board(self) -> None:
        # Placeholder for drawing the board, to be implemented with Pygame
        pass