import pygame
from grid import Grid
from score import Score

class Game:
    def __init__(self) -> None:
        self.grid = Grid()
        self.score = Score()
        self.undo_history = []
        self.load_game_state()  # Load game state at the start

    def select_block(self, x: int, y: int) -> None:
        selected_blocks = self.grid.get_selected_blocks(x, y)
        if selected_blocks:
            connected_blocks = self.grid.connect_blocks(x, y)
            if connected_blocks:
                self.clear_selected(connected_blocks)

    def clear_selected(self, selected_blocks) -> None:
        blocks_cleared = len(selected_blocks)
        self.grid.clear_blocks(selected_blocks)
        self.update_score(blocks_cleared)
        self.grid.fall_blocks()
        self.grid.generate_new_blocks()
        self.undo_history.append(selected_blocks)

    def undo_move(self) -> None:
        if self.undo_history:
            last_move = self.undo_history.pop()
            self.grid.restore_blocks(last_move)
            self.score.update_score(-len(last_move) * 10)  # Deduct points for undo

    def update_score(self, blocks_cleared: int) -> None:
        points = blocks_cleared * 10  # Example scoring logic
        self.score.update_score(points)

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as file:
                lines = file.readlines()
                self.score.current_score = int(lines[0].strip().split('=')[1])  # Load score
                self.grid.load_from_data(lines[1:])  # Load grid state
        except FileNotFoundError:
            pass

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as file:
            file.write(f'score={self.score.current_score}\n')
            file.write(self.grid.save_to_data())

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.select_block(x // 50, y // 50)  # Assuming each block is 50x50 pixels
            self.grid.display()
            pygame.display.flip()
        self.save_game_state()