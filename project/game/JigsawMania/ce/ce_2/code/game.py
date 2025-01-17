import pygame
import json
from typing import List

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def stop(self) -> None:
        self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def get_time(self) -> int:
        return self.elapsed_time

class Piece:
    def __init__(self, id: int, image: pygame.Surface) -> None:
        self.id = id
        self.image = image
        self.is_placed = False

    def drag(self) -> None:
        # Logic to drag the piece
        pass

    def drop(self) -> None:
        # Logic to drop the piece
        pass

class Game:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.timer = Timer()
        self.current_image = ""
        self.difficulty = ""

    def start_game(self, image: str, difficulty: str) -> None:
        self.current_image = image
        self.difficulty = difficulty
        self.load_progress()
        self.timer.start()

    def save_progress(self) -> None:
        progress_data = {
            "current_image": self.current_image,
            "difficulty": self.difficulty,
            "pieces": [{"id": piece.id, "is_placed": piece.is_placed} for piece in self.pieces]
        }
        with open('progress.txt', 'w') as f:
            json.dump(progress_data, f)

    def load_progress(self) -> None:
        try:
            with open('progress.txt', 'r') as f:
                progress_data = json.load(f)
                self.current_image = progress_data['current_image']
                self.difficulty = progress_data['difficulty']
                self.pieces = [Piece(piece['id'], pygame.Surface((100, 100))) for piece in progress_data['pieces']]
        except FileNotFoundError:
            print("Progress file not found. Starting a new game.")

    def rotate_piece(self, piece: Piece) -> None:
        # Logic to rotate the piece
        pass

    def restart_game(self) -> None:
        self.pieces.clear()
        self.start_game(self.current_image, self.difficulty)