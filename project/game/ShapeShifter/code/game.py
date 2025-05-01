import pygame
from shapes import ShapeManager
from target_pattern import TargetPattern
from game_state import GameState

class Game:
    def __init__(self):
        self.shape_manager = ShapeManager()
        self.target_pattern = TargetPattern()
        self.game_state = GameState()
        self.current_shapes = []
        self.selected_shape = None

    def start_game(self):
        self.shape_manager.load_shapes('shapes.txt')
        self.target_pattern.load_pattern('target_pattern.txt')
        self.game_state.load_state('game_state.txt')
        self.main_loop()

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Rotate shape on 'R' key press
                        self.rotate_shape()
                    # Additional key handling can be added here
            # Game logic and rendering would go here
            pygame.display.flip()

    def reset_game(self):
        self.current_shapes.clear()
        self.shape_manager.load_shapes('shapes.txt')  # Reload shapes after clearing
        self.game_state.save_state('game_state.txt')

    def check_match(self):
        return self.verify_match_with_target_pattern()

    def position_shape(self, shape_type: str, x: int, y: int) -> None:
        shape = self.shape_manager.get_shape(shape_type)
        shape.set_position((x, y))
        self.current_shapes.append(shape)

    def rotate_shape(self):
        if self.current_shapes:
            self.current_shapes[-1].rotate()  # Rotate the last shape in the current shapes

    def verify_match_with_target_pattern(self):
        current_arrangement = [shape.type for shape in self.current_shapes]
        return self.target_pattern.is_match(current_arrangement)

    def select_shape(self, shape_id: int):
        self.selected_shape = self.shape_manager.get_shape(shape_id)

    def reset_puzzle(self) -> None:
        for shape in self.current_shapes:
            shape.set_position((0, 0))  # Reset to initial coordinates