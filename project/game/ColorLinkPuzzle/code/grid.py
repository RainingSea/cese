import random
from block import Block

class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.blocks = [[Block(color=self.random_color(), position=(x, y)) for x in range(width)] for y in range(height)]

    def display(self):
        # Logic to display the grid
        for row in self.blocks:
            for block in row:
                block.draw()

    def reset(self):
        self.blocks = [[Block(color=self.random_color(), position=(x, y)) for x in range(self.width)] for y in range(self.height)]

    def is_path_clear(self, start: Block, end: Block) -> bool:
        return start.is_adjacent(end) and not self.is_blocked_path(start, end)

    def clear_connected_blocks(self, start_block: Block = None):
        cleared = 0
        if start_block:
            cleared += self._clear_block(start_block)
        else:
            for row in self.blocks:
                for block in row:
                    cleared += self._clear_block(block)
        print("Clearing connected blocks...")
        return cleared

    def _clear_block(self, block: Block) -> int:
        # Implement logic to check and clear connected blocks
        if block.color:  # Assuming a block is cleared if it has a color
            block.color = None  # Clear the block
            return 1
        return 0

    def is_blocked_path(self, start: Block, end: Block) -> bool:
        # Implement logic to determine if the path is blocked
        return False  # Placeholder for actual logic

    def random_color(self):
        return random.choice(['red', 'green', 'blue', 'yellow', 'purple'])

    def get_block(self, position: tuple) -> Block:
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[y][x]
        return None