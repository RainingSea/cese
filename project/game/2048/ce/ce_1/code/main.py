import pygame
import random

class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.running = True
        self.window_size = 400
        self.tile_colors = {
            0: (205, 193, 180),
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
        self.font = pygame.font.Font(None, 40)

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption('2048 Game')
        self.generate_tile()
        self.generate_tile()
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            if self.check_game_over():
                self.running = False
                self.show_game_over()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move('up')
                elif event.key == pygame.K_DOWN:
                    self.move('down')
                elif event.key == pygame.K_LEFT:
                    self.move('left')
                elif event.key == pygame.K_RIGHT:
                    self.move('right')

    def move(self, direction):
        if direction == 'up':
            self.transpose_board()
            self.merge_tiles()
            self.transpose_board()
        elif direction == 'down':
            self.transpose_board()
            self.reverse_board()
            self.merge_tiles()
            self.reverse_board()
            self.transpose_board()
        elif direction == 'left':
            self.merge_tiles()
        elif direction == 'right':
            self.reverse_board()
            self.merge_tiles()
            self.reverse_board()

        self.generate_tile()

    def transpose_board(self):
        self.board = [list(row) for row in zip(*self.board)]

    def reverse_board(self):
        self.board = [row[::-1] for row in self.board]

    def merge_tiles(self):
        for i in range(4):
            new_row = [x for x in self.board[i] if x != 0]
            merged_row = []
            skip = False
            for j in range(len(new_row)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(new_row) and new_row[j] == new_row[j + 1]:
                    merged_row.append(new_row[j] * 2)
                    self.score += new_row[j] * 2
                    skip = True
                else:
                    merged_row.append(new_row[j])
            merged_row += [0] * (4 - len(merged_row))
            self.board[i] = merged_row

    def generate_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def show_game_over(self):
        game_over_surface = self.font.render('Game Over!', True, (255, 0, 0))
        self.screen.blit(game_over_surface, (self.window_size // 2 - game_over_surface.get_width() // 2, self.window_size // 2 - game_over_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            for row in self.board:
                f.write(','.join(map(str, row)) + '\n')
            f.write(f'score={self.score}\n')

    def load_game_state(self):
        with open('game_state.txt', 'r') as f:
            lines = f.readlines()
            for i in range(4):
                self.board[i] = list(map(int, lines[i].strip().split(',')))
            self.score = int(lines[4].strip().split('=')[1])

if __name__ == "__main__":
    game = Game()
    game.start_game()