import json
from shape import Shape

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def create_shape(self, shape_type, position, size, style):
        shape_id = len(self.shapes) + 1
        new_shape = Shape(shape_id, shape_type, position, size, style)
        self.shapes.append(new_shape)
        return new_shape

    def edit_shape(self, shape_id, new_size, new_position, new_style):
        for shape in self.shapes:
            if shape.id == shape_id:
                shape.resize(new_size)
                shape.reposition(new_position)
                shape.apply_style(new_style)
                break

    def group_shapes(self, ids):
        grouped_shape = Shape(len(self.shapes) + 1, 'group', (0, 0), (0, 0), {'color': 'grey'})
        for shape_id in ids:
            for shape in self.shapes:
                if shape.id == shape_id:
                    grouped_shape.position = (min(grouped_shape.position[0], shape.position[0]),
                                              min(grouped_shape.position[1], shape.position[1]))
                    grouped_shape.size = (max(grouped_shape.size[0], shape.position[0] + shape.size[0] - grouped_shape.position[0]),
                                          max(grouped_shape.size[1], shape.position[1] + shape.size[1] - grouped_shape.position[1]))
                    break
        self.shapes.append(grouped_shape)

    def align_shapes(self, alignment_type):
        if alignment_type == 'left':
            min_x = min(shape.position[0] for shape in self.shapes)
            for shape in self.shapes:
                shape.reposition((min_x, shape.position[1]))
        elif alignment_type == 'center':
            avg_x = sum(shape.position[0] for shape in self.shapes) / len(self.shapes)
            for shape in self.shapes:
                shape.reposition((avg_x - shape.size[0] / 2, shape.position[1]))
        elif alignment_type == 'right':
            max_x = max(shape.position[0] + shape.size[0] for shape in self.shapes)
            for shape in self.shapes:
                shape.reposition((max_x - shape.size[0], shape.position[1]))

    def save_shapes(self):
        with open('shapes.json', 'w') as f:
            json.dump([{'id': shape.id, 'type': shape.type, 'position': shape.position, 'size': shape.size, 'style': shape.style} for shape in self.shapes], f)

    def load_shapes(self):
        try:
            with open('shapes.json', 'r') as f:
                shapes_data = json.load(f)
                self.shapes.clear()  # Clear existing shapes before loading
                for shape_data in shapes_data:
                    self.shapes.append(Shape(shape_data['id'], shape_data['type'], shape_data['position'], shape_data['size'], shape_data['style']))
        except FileNotFoundError:
            print("Shapes file not found. Starting with an empty shape list.")