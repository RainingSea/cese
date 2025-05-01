import pygame
import random

class Tile:
    def __init__(self, value):
        self.value = value

    def draw(self, surface, position):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.value), True, (255, 255, 255))
        rect = pygame.Rect(position[0], position[1], 100, 100)
        pygame.draw.rect(surface, self.get_color(), rect)
        surface.blit(text, (position[0] + 25, position[1] + 25))

    def get_color(self):
        colors = {
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
        }
        return colors.get(self.value, (0, 0, 0))

class Game:
    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.initialize_board()

    def initialize_board(self):
        self.generate_tile()
        self.generate_tile()

    def move(self, direction):
        if direction in ["up", "down", "left", "right"]:
            self.move_tiles(direction)
            self.generate_tile()

    def move_tiles(self, direction):
        if direction == "up":
            for col in range(4):
                self.merge_tiles(col, 0, 1)
        elif direction == "down":
            for col in range(4):
                self.merge_tiles(col, 3, -1)
        elif direction == "left":
            for row in range(4):
                self.merge_tiles(0, row, 1)
        elif direction == "right":
            for row in range(4):
                self.merge_tiles(3, row, -1)

    def merge_tiles(self, start, fixed, step):
        tiles = []
        for i in range(4):
            tile = self.board[i][fixed] if step == 1 else self.board[3 - i][fixed] if fixed == 3 else self.board[i][3]
            if tile is not None:
                tiles.append(tile)

        merged_tiles = []
        skip = False
        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            if i + 1 < len(tiles) and tiles[i].value == tiles[i + 1].value:
                new_tile = Tile(tiles[i].value * 2)
                merged_tiles.append(new_tile)
                self.score += new_tile.value
                skip = True
            else:
                merged_tiles.append(tiles[i])

        for i in range(4):
            if step == 1:
                self.board[i][fixed] = merged_tiles[i] if i < len(merged_tiles) else None
            else:
                self.board[3 - i][fixed] = merged_tiles[i] if i < len(merged_tiles) else None

    def generate_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] is None]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = Tile(random.choice([2, 4]))

    def check_game_over(self):
        if any(None in row for row in self.board):
            return False
        for r in range(4):
            for c in range(4):
                if (r < 3 and self.board[r][c].value == self.board[r + 1][c].value) or \
                   (c < 3 and self.board[r][c].value == self.board[r][c + 1].value):
                    return False
        self.display_game_over()
        return True

    def display_game_over(self):
        print("Game Over! Your score was:", self.score)

    def save_game_state(self, file_path):
        with open(file_path, 'w') as f:
            for row in self.board:
                f.write('|'.join(str(tile.value) if tile else 'None' for tile in row) + '\n')
            f.write(str(self.score) + '\n')

    def load_game_state(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for r in range(4):
                values = lines[r].strip().split('|')
                self.board[r] = [Tile(int(value)) if value != 'None' else None for value in values]
            self.score = int(lines[4].strip())