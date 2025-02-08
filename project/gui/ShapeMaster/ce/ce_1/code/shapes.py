import json

class Shape:
    def __init__(self, shape_type: str, properties: dict):
        self.type = shape_type
        self.properties = properties

    def draw(self, canvas):
        # Drawing logic will depend on the shape type and properties
        pass

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        self.shapes.remove(shape)

    def get_shapes(self):
        return self.shapes

    def load_shapes(self, file_path: str):
        with open(file_path, 'r') as file:
            shapes_data = json.load(file)
            for shape_data in shapes_data:
                shape = Shape(shape_data['type'], shape_data['properties'])
                self.add_shape(shape)

    def save_shapes(self, file_path: str):
        shapes_data = [{'type': shape.type, 'properties': shape.properties} for shape in self.shapes]
        with open(file_path, 'w') as file:
            json.dump(shapes_data, file, indent=4)