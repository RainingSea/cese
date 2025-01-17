from PIL import Image

class Layer:
    def __init__(self, id: int):
        self.id = id
        self.content = Image.new('RGBA', (800, 600), (255, 255, 255, 0))

    def draw_content(self, content: Image):
        self.content = content