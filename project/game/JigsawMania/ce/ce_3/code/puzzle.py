import pygame
import json
import os
from typing import List

class Piece:
    def __init__(self, image: pygame.Surface, position: tuple):
        self.image = image
        self.position = position

    def move(self, new_position: tuple) -> None:
        self.position = new_position

class Puzzle:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.image = None

    def create_puzzle(self, image_path: str, difficulty: str) -> None:
        # Load the image and create pieces based on difficulty
        self.image = pygame.image.load(image_path)
        # For simplicity, let's assume difficulty affects the number of pieces
        num_pieces = 4 if difficulty == 'easy' else 9  # 2x2 or 3x3
        piece_width = self.image.get_width() // int(num_pieces**0.5)
        piece_height = self.image.get_height() // int(num_pieces**0.5)

        for i in range(int(num_pieces**0.5)):
            for j in range(int(num_pieces**0.5)):
                piece_image = self.image.subsurface(j * piece_width, i * piece_height, piece_width, piece_height)
                piece = Piece(piece_image, (j * piece_width, i * piece_height))
                self.pieces.append(piece)

    def rotate_piece(self, index: int) -> None:
        if 0 <= index < len(self.pieces):
            self.pieces[index].image = pygame.transform.rotate(self.pieces[index].image, 90)

    def check_completion(self) -> bool:
        # Check if pieces are in the correct position
        for piece in self.pieces:
            if piece.position != (piece.image.get_rect().x, piece.image.get_rect().y):
                return False
        return True