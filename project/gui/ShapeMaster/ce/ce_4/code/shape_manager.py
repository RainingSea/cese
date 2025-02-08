import json
from shapes import Shape, Group

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def create_shape(self, shape_type: str, position: tuple, size: tuple, style: dict) -> Shape:
        shape = Shape(shape_type, position, size, style)
        self.shapes.append(shape)
        return shape

    def edit_shape(self, shape_id: int, new_properties: dict):
        if 0 <= shape_id < len(self.shapes):
            shape = self.shapes[shape_id]
            shape.position = new_properties.get('position', shape.position)
            shape.size = new_properties.get('size', shape.size)
            shape.style = new_properties.get('style', shape.style)

    def group_shapes(self, shape_ids: list) -> Group:
        grouped_shapes = [self.shapes[i] for i in shape_ids if 0 <= i < len(self.shapes)]
        return Group(grouped_shapes)

    def align_shapes(self, alignment_type: str):
        # Alignment logic would go here
        pass

    def save_shapes_to_file(self, filename: str):
        with open(filename, 'w') as file:
            json.dump([shape.__dict__ for shape in self.shapes], file)

    def load_shapes_from_file(self, filename: str):
        with open(filename, 'r') as file:
            shapes_data = json.load(file)
            self.shapes = [Shape(**data) for data in shapes_data]