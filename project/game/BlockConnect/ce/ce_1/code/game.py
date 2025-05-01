import pygame
from grid import Grid
from score import Score
from move import Move

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.move_history = []

    def select_block(self, x: int, y: int):
        block = self.grid.blocks[y][x]
        if block:
            self.move_history.append(Move("select", block))
            self.connect_blocks()

    def connect_blocks(self):
        connected_blocks = self.grid.get_connected_blocks()
        if connected_blocks:
            self.clear_blocks(connected_blocks)

    def clear_blocks(self, blocks):
        points = len(blocks) * 10  # Example scoring logic
        self.score.update_score(points)
        self.grid.clear(blocks)
        self.fall_blocks()

    def fall_blocks(self):
        self.grid.fall()

    def undo_move(self):
        if self.move_history:
            last_move = self.move_history.pop()
            last_move.execute()

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            f.write(self.grid.serialize())

    def load_game_state(self):
        with open('game_state.txt', 'r') as f:
            state = f.read()
            self.grid.deserialize(state)

    def run(self):
        # Game loop placeholder
        pass