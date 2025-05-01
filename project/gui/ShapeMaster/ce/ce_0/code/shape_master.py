import json
from shapes import Shape

class ShapeMaster:
    def __init__(self):
        self._shapes = []

    def create_shape(self, shape_type: str, position: tuple, size: tuple, style: dict):
        shape_id = len(self._shapes) + 1
        new_shape = Shape(shape_id, shape_type, position, size, style)
        self._shapes.append(new_shape)

    def edit_shape(self, shape_id: int, new_size: tuple, new_position: tuple, new_style: dict):
        for shape in self._shapes:
            if shape._id == shape_id:
                shape.resize(new_size)
                shape.reposition(new_position)
                shape.apply_style(new_style)
                break

    def save_shapes(self, filename: str = 'shapes.json'):
        shapes_data = [{
            'id': shape._id,
            'type': shape._type,
            'position': shape._position,
            'size': shape._size,
            'style': shape._style
        } for shape in self._shapes]
        with open(filename, 'w') as f:
            json.dump(shapes_data, f)

    def load_shapes(self, filename: str = 'shapes.json'):
        try:
            with open(filename, 'r') as f:
                shapes_data = json.load(f)
                for shape in shapes_data:
                    self.create_shape(shape['type'], tuple(shape['position']), tuple(shape['size']), shape['style'])
        except FileNotFoundError:
            print("File not found. Starting with an empty shape list.")