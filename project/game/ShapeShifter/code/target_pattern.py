class TargetPattern:
    def __init__(self):
        self.target_shapes = []

    def load_pattern(self, file_path):
        self.target_shapes.clear()  # Clear existing patterns before loading
        with open(file_path, 'r') as file:
            for line in file:
                shape_type = line.strip()
                self.target_shapes.append(shape_type)

    def is_match(self, current_shapes):
        if len(current_shapes) != len(self.target_shapes):
            return False
        return all(shape == self.target_shapes[i] for i, shape in enumerate(current_shapes))