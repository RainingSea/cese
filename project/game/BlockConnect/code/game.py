import pygame
import json
from typing import List, Tuple

class Block:
    def __init__(self, color: str) -> None:
        self.color = color

class Score:
    def __init__(self) -> None:
        self.current_score = 0

    def increment_score(self, points: int) -> None:
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score

class Grid:
    def __init__(self) -> None:
        self.blocks: List[List[Block]] = [['' for _ in range(5)] for _ in range(5)]

    def initialize_grid(self) -> None:
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        for row in range(5):
            for col in range(5):
                self.blocks[row][col] = Block(colors[(row + col) % len(colors)])

    def fall_blocks(self) -> None:
        for col in range(5):
            empty_slots = 0
            for row in range(4, -1, -1):
                if self.blocks[row][col] == '':
                    empty_slots += 1
                elif empty_slots > 0:
                    self.blocks[row + empty_slots][col] = self.blocks[row][col]
                    self.blocks[row][col] = ''

    def get_block(self, x: int, y: int) -> Block:
        return self.blocks[x][y]

class Game:
    def __init__(self) -> None:
        self.grid = Grid()
        self.score = Score()
        self.selected_blocks: List[Block] = []
        self.history: List[List[List[Block]]] = []
        self.grid.initialize_grid()

    def start_game(self) -> None:
        self.load_game_state()
        self.display_grid()
        # Main game loop would go here

    def display_grid(self) -> None:
        for row in range(len(self.grid.blocks)):
            for col in range(len(self.grid.blocks[row])):
                block = self.grid.blocks[row][col]
                print(f"Block at ({row}, {col}): {block.color if block else 'Empty'}")

    def select_block(self, x: int, y: int) -> None:
        block = self.grid.get_block(x, y)
        if block and block not in self.selected_blocks:
            self.selected_blocks.append(block)
            print(f"Selected block at ({x}, {y}): {block.color}")

    def clear_blocks(self) -> None:
        if self.selected_blocks:
            points = len(self.selected_blocks) * 10
            self.update_score(len(self.selected_blocks))
            print(f"Cleared {len(self.selected_blocks)} blocks for {points} points!")
            self.history.append([row[:] for row in self.grid.blocks])  # Save current state before clearing
            self.selected_blocks.clear()
            self.update_grid()

    def update_grid(self) -> None:
        self.grid.fall_blocks()
        self.display_grid()

    def undo_move(self) -> None:
        if self.history:
            self.grid.blocks = self.history.pop()  # Restore last state
            print("Undid last move.")
            self.display_grid()

    def save_game_state(self) -> None:
        data = {
            'grid': [[block.color if block else '' for block in row] for row in self.grid.blocks],
            'score': self.score.get_score()
        }
        with open('game_state.txt', 'w') as f:
            json.dump(data, f)

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                data = json.load(f)
                if 'grid' in data and 'score' in data:
                    self.grid.blocks = [[Block(color) if color else '' for color in row] for row in data['grid']]
                    self.score.current_score = data['score']
                else:
                    print("Invalid game state format. Starting a new game.")
                    self.grid.initialize_grid()
        except FileNotFoundError:
            print("No saved game state found. Starting a new game.")
            self.grid.initialize_grid()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}. Starting a new game.")
            self.grid.initialize_grid()

    def connect_blocks(self, positions: List[Tuple[int, int]]) -> None:
        if not positions:
            return
        color = self.grid.get_block(positions[0][0], positions[0][1]).color
        for pos in positions:
            self.grid.blocks[pos[0]][pos[1]] = Block(color)
        self.score.increment_score(len(positions))

    def update_score(self, cleared: int) -> None:
        self.score.increment_score(cleared)