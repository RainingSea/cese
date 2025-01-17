import json
from timer import Timer
from puzzle_piece import PuzzlePiece

class Game:
    def __init__(self):
        self.pieces = []
        self.timer = Timer()
        self.image_path = ""

    def load_puzzle(self, image_path: str, difficulty: str):
        self.image_path = image_path
        # Load pieces based on difficulty (not implemented, placeholder)
        self.pieces = [PuzzlePiece(i, f"{image_path}_piece_{i}.png") for i in range(1, 10)]

    def save_progress(self, user_id: str):
        progress_data = {
            "user_id": user_id,
            "pieces": [{"id": piece.id, "is_placed": piece.is_placed} for piece in self.pieces],
            "elapsed_time": self.timer.get_elapsed_time()
        }
        with open('progress.txt', 'a') as file:
            file.write(json.dumps(progress_data) + '\n')

    def load_progress(self, user_id: str):
        with open('progress.txt', 'r') as file:
            for line in file:
                progress = json.loads(line)
                if progress['user_id'] == user_id:
                    self.pieces = [PuzzlePiece(piece['id'], f"image_path_piece_{piece['id']}.png") for piece in progress['pieces']]
                    for piece in self.pieces:
                        piece.is_placed = piece['is_placed']
                    self.timer.elapsed_time = progress['elapsed_time']
                    break

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()