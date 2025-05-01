import pygame
from grid import Grid
from timer import Timer
from difficulty import Difficulty

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.difficulty = Difficulty()
        self.running = True

    def start_game(self):
        self.timer.start()
        self.load_puzzle(self.difficulty.get_level())

    def reset_game(self):
        self.grid.clear()
        self.timer = Timer()  # Reset timer
        self.start_game()

    def load_puzzle(self, difficulty: str):
        puzzle = self.difficulty.get_puzzles(difficulty)
        if puzzle:  # Ensure puzzle is valid
            self.grid.load(puzzle)
        else:
            print("No valid puzzles available for the selected difficulty.")

    def validate_input(self, row: int, col: int, symbol: str) -> bool:
        if self.grid.update_cell(row, col, symbol):
            return True
        return False

    def timer_method_flow(self):
        self.timer.start()
        # Simulate gameplay and puzzle solving
        self.timer.stop()

    def get_time_taken(self) -> str:
        return self.timer.get_time()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                        row, col = self.get_selected_cell()  # Placeholder for actual cell selection logic
                        if not self.validate_input(row, col, event.unicode):
                            print("Invalid input. Please try again.")
            self.grid.display()
            pygame.display.flip()

    def get_selected_cell(self):
        # Placeholder for actual logic to get the currently selected cell
        return 0, 0