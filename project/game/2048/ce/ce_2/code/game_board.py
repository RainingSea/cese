import random

class GameBoard:
    def __init__(self):
        self.tiles = [[0] * 4 for _ in range(4)]

    def initialize_board(self):
        self.tiles = [[0] * 4 for _ in range(4)]  # Reset the board
        self.generate_new_tile()
        self.generate_new_tile()

    def move_tiles(self, direction: str):
        if direction == 'up':
            self.tiles = self._move_up(self.tiles)
        elif direction == 'down':
            self.tiles = self._move_down(self.tiles)
        elif direction == 'left':
            self.tiles = self._move_left(self.tiles)
        elif direction == 'right':
            self.tiles = self._move_right(self.tiles)

    def _move_up(self, tiles):
        # Logic to move tiles up
        new_tiles = [row[:] for row in tiles]  # Create a copy of the current state
        for col in range(4):
            stack = []
            for row in range(4):
                if tiles[row][col] != 0:
                    stack.append(tiles[row][col])
            merged = self._merge_tiles(stack)
            for row in range(4):
                new_tiles[row][col] = merged[row] if row < len(merged) else 0
        return new_tiles

    def _move_down(self, tiles):
        new_tiles = [row[:] for row in tiles]  # Create a copy of the current state
        for col in range(4):
            stack = []
            for row in range(3, -1, -1):
                if tiles[row][col] != 0:
                    stack.append(tiles[row][col])
            merged = self._merge_tiles(stack)
            for row in range(4):
                new_tiles[3 - row][col] = merged[row] if row < len(merged) else 0
        return new_tiles

    def _move_left(self, tiles):
        new_tiles = [row[:] for row in tiles]  # Create a copy of the current state
        for row in range(4):
            stack = []
            for col in range(4):
                if tiles[row][col] != 0:
                    stack.append(tiles[row][col])
            merged = self._merge_tiles(stack)
            for col in range(4):
                new_tiles[row][col] = merged[col] if col < len(merged) else 0
        return new_tiles

    def _move_right(self, tiles):
        new_tiles = [row[:] for row in tiles]  # Create a copy of the current state
        for row in range(4):
            stack = []
            for col in range(3, -1, -1):
                if tiles[row][col] != 0:
                    stack.append(tiles[row][col])
            merged = self._merge_tiles(stack)
            for col in range(4):
                new_tiles[row][3 - col] = merged[col] if col < len(merged) else 0
        return new_tiles

    def _merge_tiles(self, stack):
        merged = []
        skip = False
        for i in range(len(stack)):
            if skip:
                skip = False
                continue
            if i + 1 < len(stack) and stack[i] == stack[i + 1]:
                merged.append(stack[i] * 2)
                skip = True
            else:
                merged.append(stack[i])
        return merged

    def generate_new_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.tiles[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.tiles[i][j] = random.choice([2, 4])

    def check_game_over(self) -> bool:
        if any(0 in row for row in self.tiles):
            return False
        for row in range(4):
            for col in range(4):
                if (col < 3 and self.tiles[row][col] == self.tiles[row][col + 1]) or \
                   (row < 3 and self.tiles[row][col] == self.tiles[row + 1][col]):
                    return False
        return True

    def get_score_increment(self) -> int:
        # Return the score increment based on the last move
        return sum(tile for row in self.tiles for tile in row if tile != 0)  # Example logic