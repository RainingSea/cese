import pygame
import json

class Puzzle:
    def __init__(self):
        self.pieces = []

    def create_puzzle(self, image_path: str, difficulty: str) -> None:
        # Load image and create pieces based on difficulty
        self.pieces = self.load_pieces(image_path, difficulty)

    def load_pieces(self, image_path: str, difficulty: str):
        # Logic to create pieces from the image based on difficulty
        return []

    def rotate_piece(self, index: int) -> None:
        if 0 <= index < len(self.pieces):
            self.pieces[index].rotate()

    def check_completion(self) -> bool:
        # Logic to check if the puzzle is completed
        return all(piece.is_in_correct_position() for piece in self.pieces)

    def get_state(self):
        # Return the current state of the puzzle
        return [piece.get_state() for piece in self.pieces]

    def load_state(self, state):
        # Load the puzzle state
        for piece_state in state:
            piece = Piece()
            piece.load_state(piece_state)
            self.pieces.append(piece)