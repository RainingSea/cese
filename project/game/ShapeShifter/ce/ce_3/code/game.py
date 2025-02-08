import json

class Shape:
    def __init__(self, shape_type: str, position: tuple, rotation: int):
        self.type = shape_type
        self.position = position
        self.rotation = rotation

    def rotate(self, angle: int):
        self.rotation = (self.rotation + angle) % 360

    def set_position(self, position: tuple):
        self.position = position


class Game:
    def __init__(self, shapes: list, target_pattern: list):
        self.shapes = shapes
        self.target_pattern = target_pattern

    def select_shape(self, shape: Shape):
        if shape in self.shapes:
            return shape
        return None

    def rotate_shape(self, shape: Shape, angle: int):
        shape.rotate(angle)

    def position_shape(self, shape: Shape, position: tuple):
        shape.set_position(position)

    def verify_arrangement(self) -> bool:
        current_pattern = [(shape.type, shape.position, shape.rotation) for shape in self.shapes]
        return current_pattern == self.target_pattern

    def reset_puzzle(self):
        for shape in self.shapes:
            shape.set_position((0, 0))
            shape.rotation = 0

    def save_game_state(self):
        game_state = {
            'shapes': [(shape.type, shape.position, shape.rotation) for shape in self.shapes]
        }
        with open('game_state.txt', 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self):
        with open('game_state.txt', 'r') as f:
            game_state = json.load(f)
            for shape_data in game_state['shapes']:
                shape = Shape(shape_data[0], shape_data[1], shape_data[2])
                self.shapes.append(shape)