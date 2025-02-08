import pygame
import json

class Tile:
    def __init__(self, color: str, pattern: str):
        self.color = color
        self.pattern = pattern

class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def update_score(self, points: int):
        self.score += points

class Board:
    def __init__(self, size: int):
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def display_board(self):
        for row in self.grid:
            print(' | '.join([' ' if tile is None else tile.pattern for tile in row]))

    def update_board(self, tile: Tile, position: tuple):
        x, y = position
        self.grid[y][x] = tile

class Game:
    def __init__(self):
        self.board = Board(size=5)
        self.available_tiles = [Tile('red', 'A'), Tile('blue', 'B'), Tile('green', 'C')]
        self.players = [Player('Player 1'), Player('Player 2')]
        self.current_turn = 0
        self.history = []

    def start_game(self):
        print("Game started!")
        self.board.display_board()

    def place_tile(self, player: Player, tile: Tile, position: tuple):
        self.board.update_board(tile, position)
        self.history.append((player, tile, position))
        print(f"{player.name} placed {tile.pattern} at {position}")

    def calculate_points(self) -> int:
        # Placeholder for point calculation logic
        return 0

    def undo_last_action(self):
        if self.history:
            last_action = self.history.pop()
            player, tile, position = last_action
            self.board.update_board(None, position)
            print(f"{player.name} undid the last action of placing {tile.pattern} at {position}")

    def save_game(self):
        game_state = {
            'board': [[tile.pattern if tile else None for tile in row] for row in self.board.grid],
            'current_turn': self.current_turn,
            'players': [(player.name, player.score) for player in self.players]
        }
        with open('game_state.txt', 'w') as f:
            json.dump(game_state, f)
        print("Game state saved.")

    def load_game(self):
        try:
            with open('game_state.txt', 'r') as f:
                game_state = json.load(f)
                self.board.grid = [[Tile('red', pattern) if pattern else None for pattern in row] for row in game_state['board']]
                self.current_turn = game_state['current_turn']
                self.players = [Player(name) for name, _ in game_state['players']]
                for player, score in game_state['players']:
                    self.players[self.players.index(player)].score = score
            print("Game state loaded.")
        except FileNotFoundError:
            print("No saved game state found.")