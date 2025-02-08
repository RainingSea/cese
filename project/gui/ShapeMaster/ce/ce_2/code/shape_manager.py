import json
from shapes import Shape

class ShapeManager:
    def __init__(self) -> None:
        self.shapes = []

    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape) -> None:
        self.shapes.remove(shape)

    def edit_shape(self, shape: Shape, properties: dict) -> None:
        shape.apply_style(properties)

    def load_shapes(self) -> None:
        try:
            with open('shapes.json', 'r') as file:
                shapes_data = json.load(file)
                for shape_data in shapes_data:
                    shape = Shape(shape_data['type'], shape_data['properties'])
                    self.add_shape(shape)
        except FileNotFoundError:
            pass

    def save_shapes(self) -> None:
        shapes_data = [{'type': shape.shape_type, 'properties': shape.properties} for shape in self.shapes]
        with open('shapes.json', 'w') as file:
            json.dump(shapes_data, file)