import pygame

class Piece:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.is_movable = True
        self.is_rotated = False
        self.position = (0, 0)

    def move(self, new_position) -> None:
        self.position = new_position

    def rotate(self) -> None:
        self.is_rotated = not self.is_rotated

    def get_position(self):
        return self.position

    def set_position(self, position) -> None:
        self.position = position