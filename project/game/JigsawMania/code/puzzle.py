import pygame
from piece import Piece

class Puzzle:
    def __init__(self, image_path: str, difficulty: int):
        self.image_path = image_path
        self.difficulty = difficulty
        self.pieces = self.load_pieces(image_path, difficulty)

    def load_pieces(self, image_path: str, difficulty: int):
        return [Piece(image_path) for _ in range(difficulty)]  # Example based on difficulty

    def shuffle_pieces(self) -> None:
        import random
        random.shuffle(self.pieces)

    def rotate_piece(self, index: int) -> None:
        if 0 <= index < len(self.pieces):
            self.pieces[index].rotate()
    
    def create_puzzle(self, image_path: str, difficulty: int) -> None:
        self.pieces = self.load_pieces(image_path, difficulty)