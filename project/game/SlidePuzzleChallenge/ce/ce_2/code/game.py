import pygame
from grid import Grid
from timer import Timer
from hints import Hints

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.hints = Hints()
        self.difficulty = "easy"

    def start_game(self, difficulty: str) -> None:
        self.difficulty = difficulty
        self.grid.initialize_grid(difficulty)
        self.timer.start()
        self.shuffle_tiles()

    def save_progress(self) -> None:
        with open('game_state.txt', 'w') as f:
            f.write(self.grid.serialize())
            f.write(f"\n{self.timer.get_time()}")

    def load_progress(self) -> None:
        with open('game_state.txt', 'r') as f:
            data = f.readlines()
            self.grid.deserialize(data[0])
            self.timer.stop()  # Assuming we want to stop the timer when loading

    def shuffle_tiles(self) -> None:
        self.grid.shuffle()

    def provide_hint(self) -> str:
        return self.hints.generate_hint(self.grid)

    def reset_game(self) -> None:
        self.grid.reset()
        self.shuffle_tiles()