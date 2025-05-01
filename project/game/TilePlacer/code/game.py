import pygame
import os
from typing import List, Tuple

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []
        self.current_turn = 0
        self.action_history = []  # To keep track of actions for undo
        self.load_game_state()
        self.load_settings()

    def start_game(self):
        self.players = self.load_players()
        self.board.display()
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # Example key for undo
                self.undo_last_action()
            elif event.key == pygame.K_n:  # Example key for next turn
                self.next_turn()
            # Add more event handling as needed

    def place_tile(self, player, tile: 'Tile', position: Tuple[int, int]):
        if self.board.is_position_valid(position):
            self.board.update_board(tile, position)
            player.update_score(1)  # Example scoring logic
            self.action_history.append((tile, position))  # Record action
            self.save_progress()

    def undo_last_action(self):
        if self.action_history:
            last_tile, last_position = self.action_history.pop()
            self.board.remove_tile(last_position)  # Remove the last placed tile
            last_player = self.players[self.current_turn]
            last_player.update_score(-1)  # Deduct score for undo
            self.save_progress()

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.save_game_state()

    def calculate_score(self) -> int:
        return sum(player.score for player in self.players)

    def save_progress(self):
        with open('game_state.txt', 'w') as f:
            f.write(f'Current Player: {self.players[self.current_turn].name}\n')
            f.write(f'Scores: {[player.score for player in self.players]}\n')
            f.write(f'Tiles: {self.board.serialize()}\n')

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            f.write(f'current_turn|{self.current_turn}\n')
            f.write(f'board_configuration|{self.board.serialize()}\n')

    def load_game_state(self):
        if os.path.exists('game_state.txt'):
            with open('game_state.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    if key == 'current_turn':
                        self.current_turn = int(value)
                    elif key == 'board_configuration':
                        self.board.deserialize(value)

    def load_players(self) -> List['Player']:
        players = []
        if os.path.exists('players.txt'):
            with open('players.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split('|')
                    players.append(Player(name, int(score)))
        return players

    def load_settings(self):
        if os.path.exists('settings.txt'):
            with open('settings.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    if key == 'tile_color':
                        self.tile_color = value
                    elif key == 'board_design':
                        self.board_design = value

class Board:
    def __init__(self):
        self.tiles = []

    def display(self):
        # Render the game board and available tiles
        pass

    def update_board(self, tile: 'Tile', position: Tuple[int, int]):
        self.tiles.append((tile, position))

    def remove_tile(self, position: Tuple[int, int]):
        self.tiles = [t for t in self.tiles if t[1] != position]

    def is_position_valid(self, position: Tuple[int, int]) -> bool:
        # Check if the position is valid for placing a tile
        return True  # Placeholder for actual validation logic

    def serialize(self) -> str:
        return ','.join(f'{tile.color}:{tile.pattern}@{pos[0]},{pos[1]}' for tile, pos in self.tiles)

    def deserialize(self, data: str):
        for item in data.split(','):
            tile_info, pos_info = item.split('@')
            color, pattern = tile_info.split(':')
            x, y = map(int, pos_info.split(','))
            tile = Tile(color, pattern)
            self.update_board(tile, (x, y))

class Player:
    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score

    def update_score(self, points: int):
        self.score += points

class Tile:
    def __init__(self, color: str, pattern: str):
        self.color = color
        self.pattern = pattern