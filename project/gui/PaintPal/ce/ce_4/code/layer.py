from PIL import Image

class Layer:
    def __init__(self, image: Image):
        self.image = image

    def merge(self) -> Image:
        # This method would contain logic to merge this layer with others
        return self.image