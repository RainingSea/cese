class Shape:
    def __init__(self, shape_id: int, shape_type: str):
        self.id = shape_id
        self.type = shape_type
        self.rotation = 0
        self.position_x = 0
        self.position_y = 0

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

    def set_position(self, x: int, y: int):
        self.position_x = x
        self.position_y = y