from PIL import Image as PILImage

class Image:
    def __init__(self, path: str):
        self.image = self.open(path)

    def open(self, path: str) -> PILImage:
        return PILImage.open(path)

    def show(self) -> None:
        self.image.show()

    def save(self, path: str) -> None:
        self.image.save(path)