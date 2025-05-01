import pygame
from grid import Grid

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = 0
        self.undo_stack = []
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.select_block(x // self.grid.block_size, y // self.grid.block_size)

    def select_block(self, x: int, y: int):
        self.grid.select_block(x, y)

    def connect_blocks(self):
        blocks_cleared = self.grid.connect_blocks()
        self.update_score(blocks_cleared)

    def update_score(self, blocks_cleared: int):
        self.score += blocks_cleared

    def undo_move(self):
        if self.undo_stack:
            previous_state = self.undo_stack.pop()
            self.grid.load_state(previous_state)

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.grid}\n{self.score}")