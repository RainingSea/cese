from block import Block

class Grid:
    def __init__(self):
        self.blocks = [[Block() for _ in range(10)] for _ in range(10)]
        self.block_size = 40

    def display(self):
        for row in self.blocks:
            for block in row:
                block.draw()

    def clear_blocks(self, blocks_to_clear):
        for block in blocks_to_clear:
            self.blocks[block.y][block.x] = None

    def drop_blocks(self):
        for col in range(len(self.blocks[0])):
            for row in range(len(self.blocks) - 1, -1, -1):
                if self.blocks[row][col] is None:
                    for r in range(row, 0, -1):
                        if self.blocks[r-1][col] is not None:
                            self.blocks[r][col] = self.blocks[r-1][col]
                            self.blocks[r-1][col] = None
                            break

    def generate_new_blocks(self):
        for col in range(len(self.blocks[0])):
            if self.blocks[0][col] is None:
                self.blocks[0][col] = Block()

    def select_block(self, x: int, y: int):
        # Logic to select a block
        pass

    def connect_blocks(self):
        # Logic to connect blocks and return number of blocks cleared
        return 0

    def load_state(self, state):
        # Logic to load a previous game state
        pass