from shapes import Shape

class Canvas:
    def __init__(self):
        self.shapes = []

    def draw_shape(self, shape: Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        self.shapes.remove(shape)

    def update_shape(self, shape: Shape):
        for idx, existing_shape in enumerate(self.shapes):
            if existing_shape.type == shape.type and existing_shape.get_properties() == shape.get_properties():
                self.shapes[idx] = shape

    def group_shapes(self, shapes: list):
        # Placeholder for grouping shapes functionality
        pass

    def arrange_shape(self, shape: Shape, position: str):
        # Placeholder for arranging shapes functionality
        pass