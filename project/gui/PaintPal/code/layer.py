class Layer:
    def __init__(self, name: str):
        self.name = name
        self.visible = True

    def draw(self, x: int, y: int):
        # Drawing logic for the layer
        pass

    def draw_on_image(self, draw):
        # Logic to draw on the image
        pass

    def toggle_visibility(self):
        self.visible = not self.visible