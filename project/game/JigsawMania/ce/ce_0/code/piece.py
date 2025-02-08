class Piece:
    def __init__(self, image, position):
        self.image = image
        self.position = position

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position