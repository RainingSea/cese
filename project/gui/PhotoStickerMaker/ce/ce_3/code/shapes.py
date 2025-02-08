class Shapes:
    """Class to define various shapes for stickers."""
    
    def __init__(self):
        self.shapes = {
            "circle": self.create_circle,
            "square": self.create_square,
            "rectangle": self.create_rectangle,
            "star": self.create_star
        }

    def create_circle(self, size):
        """Create a circle shape."""
        return {"type": "circle", "size": size}

    def create_square(self, size):
        """Create a square shape."""
        return {"type": "square", "size": size}

    def create_rectangle(self, size):
        """Create a rectangle shape."""
        return {"type": "rectangle", "size": size}

    def create_star(self, size):
        """Create a star shape."""
        return {"type": "star", "size": size}