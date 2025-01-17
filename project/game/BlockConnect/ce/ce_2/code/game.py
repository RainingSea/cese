import json
from typing import List

class Block:
    def __init__(self, color: str) -> None:
        self.color = color

class Move:
    def __init__(self, selected_blocks: List[Block]) -> None:
        self.selected_blocks = selected_blocks

class Game:
    def __init__(self) -> None:
        self.grid = [[Block("red"), Block("green"), Block("blue")],
                     [Block("green"), Block("blue"), Block("red")],
                     [Block("blue"), Block("red"), Block("green")]]
        self.score = 0
        self.history = []

    def select_block(self, x: int, y: int) -> None:
        selected_block = self.grid[x][y]
        self.clear_blocks(selected_block.color)

    def clear_blocks(self, color: str) -> None:
        cleared_blocks = []
        for row in self.grid:
            for block in row:
                if block.color == color:
                    cleared_blocks.append(block)
                    block.color = "white"  # Assume white indicates cleared
        self.history.append(Move(cleared_blocks))
        self.update_grid()
        self.score += len(cleared_blocks)

    def update_grid(self) -> None:
        # Logic to update grid after clearing blocks
        pass

    def undo(self) -> None:
        if self.history:
            last_move = self.history.pop()
            for block in last_move.selected_blocks:
                block.color = block.color  # Restore the original color
            self.score -= len(last_move.selected_blocks)

    def save_state(self) -> None:
        state = {
            "score": self.score,
            "grid": [[block.color for block in row] for row in self.grid]
        }
        with open('game_state.txt', 'w') as f:
            json.dump(state, f)

    def load_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                state = json.load(f)
                self.score = state["score"]
                for i, row in enumerate(self.grid):
                    for j, block in enumerate(row):
                        block.color = state["grid"][i][j]
        except FileNotFoundError:
            pass