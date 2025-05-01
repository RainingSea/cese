import pygame
from grid import Grid
from score import Score

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.undo_history = []

    def select_block(self, x: int, y: int):
        self.grid.select_block(x, y)
        self.connect_blocks()

    def connect_blocks(self):
        if self.grid.check_connections():
            self.clear_blocks()

    def clear_blocks(self):
        points = self.grid.clear_selected()
        self.score.update_score(points)
        self.fall_blocks()

    def fall_blocks(self):
        self.grid.fall_blocks()

    def undo_move(self):
        if self.undo_history:
            last_action = self.undo_history.pop()
            self.grid.restore_state(last_action)

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            f.write(f"score={self.score.current_score}\n")
            f.write(f"grid={self.grid.serialize()}\n")

    def load_game_state(self):
        try:
            with open('game_state.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    if key == 'score':
                        self.score.current_score = int(value)
                    elif key == 'grid':
                        self.grid.deserialize(value)
        except FileNotFoundError:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        self.grid.update()

    def render(self):
        self.grid.display()
        self.score.display()
        pygame.display.flip()