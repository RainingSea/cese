class Shape:
    def __init__(self, id: int, shape_type: str, position: tuple, size: tuple, style: dict):
        self.id = id
        self.shape_type = shape_type
        self.position = position
        self.size = size
        self.style = style

    def draw(self, canvas):
        if self.shape_type == 'rectangle':
            canvas.create_rectangle(*self.position, 
                                     self.position[0] + self.size[0], 
                                     self.position[1] + self.size[1], 
                                     **self.style)
        elif self.shape_type == 'circle':
            x, y = self.position
            r = self.size[0]  # Assuming size[0] is the radius
            canvas.create_oval(x - r, y - r, x + r, y + r, **self.style)
        elif self.shape_type == 'triangle':
            x, y = self.position
            points = [x, y, x + self.size[0], y + self.size[1], x - self.size[0], y + self.size[1]]
            canvas.create_polygon(points, **self.style)
        elif self.shape_type == 'polygon':
            points = [coord for point in self.position for coord in point]
            canvas.create_polygon(points, **self.style)

    def update_properties(self, new_position: tuple, new_size: tuple, new_style: dict):
        self.position = new_position
        self.size = new_size
        self.style = new_style