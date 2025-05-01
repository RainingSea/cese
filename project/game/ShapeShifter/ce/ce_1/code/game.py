import pygame
from shapes import Shape
from target_pattern import TargetPattern

class Game:
    def __init__(self):
        self.shapes = []
        self.target_pattern = TargetPattern()
        self.selected_shape = None
        self.running = True

    def start(self):
        self.load_shapes()
        self.game_loop()

    def load_shapes(self):
        # Load shapes from shapes.txt
        with open('shapes.txt', 'r') as file:
            for line in file:
                shape_data = line.strip().split('|')
                shape = Shape(int(shape_data[0]), shape_data[1])
                self.shapes.append(shape)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle other events like shape selection, rotation, and positioning

    def select_shape(self, shape_id: int):
        self.selected_shape = self.shapes[shape_id]

    def rotate_shape(self):
        if self.selected_shape:
            self.selected_shape.rotate()

    def position_shape(self, x: int, y: int):
        if self.selected_shape:
            self.selected_shape.set_position(x, y)

    def verify_arrangement(self) -> bool:
        return self.target_pattern.check_match(self.shapes)

    def reset_puzzle(self):
        for shape in self.shapes:
            shape.set_position(0, 0)