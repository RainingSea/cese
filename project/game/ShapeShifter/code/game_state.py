from shapes import Shape

class GameState:
    def __init__(self):
        self.current_shapes = []

    def save_state(self, file_path):
        with open(file_path, 'w') as file:
            for shape in self.current_shapes:
                file.write(f"{shape.type}|{shape.rotation}|{shape.position[0]}|{shape.position[1]}\n")

    def load_state(self, file_path):
        self.current_shapes.clear()  # Clear existing shapes before loading
        with open(file_path, 'r') as file:
            for line in file:
                shape_type, rotation, x, y = line.strip().split('|')
                self.current_shapes.append(Shape(shape_type, float(rotation)))
                self.current_shapes[-1].set_position((float(x), float(y)))