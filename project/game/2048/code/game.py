import json
from board import Board
from tile import Tile

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0

    def start_game(self) -> None:
        self.board.initialize()
        self.score = 0

    def move(self, direction: str) -> None:
        if self.board.move(direction):
            self.check_game_over()

    def save_game(self) -> None:
        game_state = {
            'board': self.board.to_dict(),
            'score': self.score
        }
        with open('game_state.txt', 'w') as f:
            json.dump(game_state, f)

    def load_game(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                game_state = json.load(f)
                self.board.tiles = [[Tile(value) if value != 0 else 0 for value in row] for row in game_state['board']['tiles']]
                self.score = game_state['score']
        except FileNotFoundError:
            print("No saved game found.")

    def check_game_over(self) -> bool:
        for row in self.board.tiles:
            if 0 in row:
                return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board.tiles[i][j] == self.board.tiles[i + 1][j]) or \
                   (j < 3 and self.board.tiles[i][j] == self.board.tiles[i][j + 1]):
                    return False
        return True