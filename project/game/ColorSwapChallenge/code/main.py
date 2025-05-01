import pygame
import random
import json

# Constants
GRID_SIZE = 8
BLOCK_COLORS = ['red', 'green', 'blue', 'yellow', 'purple']
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 70

class Block:
    def __init__(self, color):
        self.color = color

    def draw(self, surface, position):
        pygame.draw.rect(surface, self.color, (position[0], position[1], BLOCK_SIZE, BLOCK_SIZE))

class Grid:
    def __init__(self):
        self.blocks = [[self.create_block() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def create_block(self):
        return Block(random.choice(BLOCK_COLORS))

    def initialize_grid(self):
        self.blocks = [[self.create_block() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def get_block(self, pos):
        return self.blocks[pos[0]][pos[1]]

    def swap_blocks(self, pos1, pos2):
        self.blocks[pos1[0]][pos1[1]], self.blocks[pos2[0]][pos2[1]] = self.blocks[pos2[0]][pos2[1]], self.blocks[pos1[0]][pos1[1]]

    def update_grid(self):
        matches = self.check_matches()
        if matches:
            self.clear_matches(matches)
            self.fill_empty_spaces()

    def clear_matches(self, matches):
        for match in matches:
            for pos in match:
                self.blocks[pos[0]][pos[1]] = self.create_block()

    def fill_empty_spaces(self):
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 1, -1, -1):
                if self.blocks[i][j] is None:
                    for k in range(i - 1, -1, -1):
                        if self.blocks[k][j] is not None:
                            self.blocks[i][j] = self.blocks[k][j]
                            self.blocks[k][j] = None
                            break

    def check_matches(self):
        matches = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE - 2 and self.blocks[i][j].color == self.blocks[i][j + 1].color == self.blocks[i][j + 2].color:
                    matches.append([(i, j), (i, j + 1), (i, j + 2)])
                if i < GRID_SIZE - 2 and self.blocks[i][j].color == self.blocks[i + 1][j].color == self.blocks[i + 2][j].color:
                    matches.append([(i, j), (i + 1, j), (i + 2, j)])
        return matches

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, blocks_cleared, combos, moves_used):
        self.points += (blocks_cleared * 10) + (combos * 50) - (moves_used * 5)

class Level:
    def __init__(self):
        self.difficulty = 1
        self.move_limit = 10

    def load_level(self, level_number):
        with open('levels.json', 'r') as file:
            levels = json.load(file)
            level_data = levels.get(str(level_number))
            if level_data:
                self.difficulty = level_data['difficulty']
                self.move_limit = level_data['move_limit']

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.level = Level()
        self.move_counter = 0

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Block Match Game")
        self.level.load_level(1)
        self.grid.initialize_grid()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Handle block swapping logic here
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Example key for a move
                        if self.move_counter < self.level.move_limit:
                            self.move_counter += 1
                            self.clear_matches()
                        else:
                            print("Move limit reached! No more moves allowed.")
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            pygame.display.flip()

    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                block = self.grid.get_block((i, j))
                block.draw(self.screen, (j * BLOCK_SIZE, i * BLOCK_SIZE))

    def clear_matches(self):
        matches = self.grid.check_matches()
        if matches:
            blocks_cleared = sum(len(match) for match in matches)
            self.grid.clear_matches(matches)
            self.grid.update_grid()
            self.update_score(blocks_cleared, len(matches) - 1)

    def update_score(self, blocks_cleared, combos):
        self.score.calculate_score(blocks_cleared, combos, self.move_counter)

    def end_game(self):
        print("Game Over! Your score:", self.score.points)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.start_game()
    game.game_loop()
    pygame.quit()