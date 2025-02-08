import os
from piece import Piece

class Puzzle:
    def __init__(self):
        self.pieces = []

    def create_puzzle(self, image_path: str, difficulty: str):
        # Load image and create pieces based on difficulty
        # For simplicity, we will assume difficulty just determines number of pieces
        piece_count = 4 if difficulty == 'easy' else 9 if difficulty == 'medium' else 16
        image = self.load_image(image_path)
        piece_width = image.get_width() // piece_count
        piece_height = image.get_height() // piece_count
        
        for i in range(piece_count):
            for j in range(piece_count):
                piece_image = image.subsurface((j * piece_width, i * piece_height, piece_width, piece_height))
                piece = Piece(piece_image, (j, i))
                self.pieces.append(piece)

    def load_image(self, image_path: str):
        from pygame import image
        return image.load(image_path)

    def rotate_piece(self, index: int):
        from pygame.transform import rotate
        self.pieces[index].image = rotate(self.pieces[index].image, 90)

    def check_completion(self):
        return all(piece.get_position() == (index % len(self.pieces), index // len(self.pieces)) 
                   for index, piece in enumerate(self.pieces))