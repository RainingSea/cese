from typing import List, Tuple
from board import Board
from tile import Tile
from player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.available_tiles: List[Tile] = [Tile("Red"), Tile("Blue"), Tile("Green"), Tile("Yellow")]
        self.players: List[Player] = []
        self.current_player_index = 0

    def start_game(self):
        # Initialize players
        self.players.append(Player("Player 1"))
        self.players.append(Player("Player 2"))

    def place_tile(self, tile: Tile, position: Tuple[int, int]):
        self.board.update_tile(position, tile)

    def undo_last_action(self):
        # Logic to undo the last action
        pass

    def save_progress(self):
        with open('game_progress.txt', 'w') as f:
            f.write(f'Current Player Index: {self.current_player_index}\n')

    def load_progress(self):
        with open('game_progress.txt', 'r') as f:
            data = f.readlines()
            self.current_player_index = int(data[0].split(': ')[1])

    def calculate_points(self):
        # Logic to calculate points
        pass