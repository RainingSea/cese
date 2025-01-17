from timer import Timer
from score import Score
from grid import Grid

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.score = Score()

    def start_game(self, level: int) -> None:
        """Starts a new game with the specified difficulty level."""
        self.grid.generate_grid(level)
        self.timer.start_timer(60)  # 60 seconds for the game
        self.score = Score()  # Reset score

    def click_tile(self, x: int, y: int) -> None:
        """Handles tile click events."""
        # Logic for handling tile clicks goes here
        pass

    def check_path(self) -> bool:
        """Checks if the current path is valid."""
        # Logic for checking the path goes here
        return True

    def save_game_state(self) -> None:
        """Saves the current game state to a file."""
        with open('game_data.txt', 'w') as f:
            f.write(f"score|{self.score.get_score()}\n")
            f.write(f"time_remaining|{self.timer.time_remaining}\n")

    def load_game_state(self) -> None:
        """Loads the game state from a file."""
        try:
            with open('game_data.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    if key == 'score':
                        self.score.current_score = int(value)
                    elif key == 'time_remaining':
                        self.timer.time_remaining = float(value)
        except FileNotFoundError:
            print("No saved game state found.")