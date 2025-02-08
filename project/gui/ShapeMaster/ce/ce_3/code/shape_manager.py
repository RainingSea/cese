import json
from shapes import Shape

class ShapeManager:
    def __init__(self):
        self.shapes = []
        self.next_id = 1

    def create_shape(self, shape_type: str, position: tuple, size: tuple, style: dict) -> Shape:
        shape = Shape(self.next_id, shape_type, position, size, style)
        self.shapes.append(shape)
        self.next_id += 1
        return shape

    def edit_shape(self, shape_id: int, new_position: tuple, new_size: tuple, new_style: dict):
        for shape in self.shapes:
            if shape.id == shape_id:
                shape.update_properties(new_position, new_size, new_style)
                break

    def group_shapes(self, shape_ids: list):
        # Grouping logic can be implemented here
        pass

    def align_shapes(self, alignment_type: str):
        # Alignment logic can be implemented here
        pass

    def save_shapes_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump([shape.__dict__ for shape in self.shapes], file)

    def load_shapes_from_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                shapes_data = json.load(file)
                for shape_data in shapes_data:
                    shape = Shape(shape_data['id'], shape_data['shape_type'], 
                                  shape_data['position'], shape_data['size'], 
                                  shape_data['style'])
                    self.shapes.append(shape)
                    self.next_id = max(self.next_id, shape.id + 1)
        except FileNotFoundError:
            print("File not found. Starting with an empty shape list.")