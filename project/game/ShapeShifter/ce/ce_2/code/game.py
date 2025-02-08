import pygame

class Shape:
    def __init__(self, shape_type: str, rotation: int, position: tuple):
        self.type = shape_type
        self.rotation = rotation
        self.position = position

    def rotate(self) -> None:
        self.rotation = (self.rotation + 90) % 360

    def move(self, position: tuple) -> None:
        self.position = position

class Game:
    def __init__(self):
        self.shapes = []
        self.target_pattern = []
        self.is_correct = False

    def load_shapes(self) -> None:
        with open('shapes.txt', 'r') as file:
            for line in file:
                shape_data = line.strip().split('|')
                shape = Shape(shape_data[0], int(shape_data[1]), (int(shape_data[2]), int(shape_data[3])))
                self.shapes.append(shape)

    def load_patterns(self) -> None:
        with open('patterns.txt', 'r') as file:
            for line in file:
                pattern_data = line.strip().split('|')
                self.target_pattern.append((pattern_data[0], int(pattern_data[1]), (int(pattern_data[2]), int(pattern_data[3]))))

    def check_arrangement(self) -> bool:
        # Simple check based on shape type and position
        for shape in self.shapes:
            if (shape.type, shape.rotation, shape.position) not in self.target_pattern:
                return False
        return True

    def reset(self) -> None:
        self.shapes.clear()
        self.is_correct = False

    def draw(self) -> None:
        # Drawing logic using pygame would go here
        pass