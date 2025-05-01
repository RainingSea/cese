class Shape:
    def __init__(self, shape_type, rotation=0):
        self.type = shape_type
        self.rotation = rotation
        self.position = (0, 0)  # Default position

    def rotate(self):
        self.rotation += 90
        self.rotation %= 360

    def get_properties(self):
        return {'type': self.type, 'rotation': self.rotation, 'position': self.position}

    def set_position(self, pos):
        self.position = pos

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def load_shapes(self, file_path):
        self.shapes.clear()  # Clear existing shapes before loading
        with open(file_path, 'r') as file:
            for line in file:
                shape_type = line.strip()
                self.shapes.append(Shape(shape_type))

    def get_shape(self, shape_id):
        return self.shapes[int(shape_id)]