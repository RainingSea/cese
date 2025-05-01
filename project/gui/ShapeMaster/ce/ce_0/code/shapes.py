class Shape:
    def __init__(self, shape_id: int, shape_type: str, position: tuple, size: tuple, style: dict):
        self._id = shape_id
        self._type = shape_type
        self._position = position
        self._size = size
        self._style = style

    def draw(self, canvas):
        if self._type == "rectangle":
            canvas.create_rectangle(
                self._position[0], self._position[1],
                self._position[0] + self._size[0], self._position[1] + self._size[1],
                **self._style
            )
        elif self._type == "circle":
            x0 = self._position[0] - self._size[0] / 2
            y0 = self._position[1] - self._size[1] / 2
            x1 = self._position[0] + self._size[0] / 2
            y1 = self._position[1] + self._size[1] / 2
            canvas.create_oval(x0, y0, x1, y1, **self._style)

    def resize(self, new_size: tuple):
        self._size = new_size

    def reposition(self, new_position: tuple):
        self._position = new_position

    def apply_style(self, style: dict):
        self._style.update(style)