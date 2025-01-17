import json
from puzzle import Puzzle
from timer import Timer

class Game:
    def __init__(self):
        self.puzzle = Puzzle()
        self.timer = Timer()

    def start_game(self, image_path: str, difficulty: str):
        self.puzzle.create_puzzle(image_path, difficulty)
        self.timer.start()

    def save_progress(self):
        progress_data = {
            'pieces': [(piece.get_position(), piece.image) for piece in self.puzzle.pieces],
            'elapsed_time': self.timer.get_time()
        }
        with open('progress.txt', 'w') as f:
            json.dump(progress_data, f)

    def load_progress(self):
        if os.path.exists('progress.txt'):
            with open('progress.txt', 'r') as f:
                progress_data = json.load(f)
                self.puzzle.pieces = [Piece(image, pos) for pos, image in progress_data['pieces']]
                self.timer.elapsed_time = progress_data['elapsed_time']

    def restart_game(self):
        self.puzzle = Puzzle()
        self.timer = Timer()