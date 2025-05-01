class Shape:
    def __init__(self, shape_id, shape_type, position, size, style):
        self.id = shape_id
        self.type = shape_type
        self.position = position
        self.size = size
        self.style = style

    def draw(self, canvas):
        if self.type == 'rectangle':
            canvas.create_rectangle(self.position[0], self.position[1],
                                    self.position[0] + self.size[0],
                                    self.position[1] + self.size[1],
                                    fill=self.style['color'])
        elif self.type == 'circle':
            canvas.create_oval(self.position[0], self.position[1],
                               self.position[0] + self.size[0] * 2,
                               self.position[1] + self.size[0] * 2,
                               fill=self.style['color'])
        elif self.type == 'triangle':
            x1, y1 = self.position
            x2, y2 = x1 + self.size[0], y1
            x3, y3 = x1 + self.size[0] / 2, y1 - self.size[1]
            canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=self.style['color'])
        elif self.type == 'polygon':
            canvas.create_polygon(self.size['points'], fill=self.style['color'])

    def resize(self, new_size):
        self.size = new_size

    def reposition(self, new_position):
        self.position = new_position

    def apply_style(self, style):
        self.style.update(style)