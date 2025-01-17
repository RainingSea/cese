from image_processor import ImageProcessor
from user_interface import UserInterface

class StickerMaker:
    def __init__(self, master):
        self.image_processor = ImageProcessor()
        self.user_interface = UserInterface(master)

    def import_image(self, file_path: str) -> None:
        self.user_interface.import_image()

    def set_shape(self, shape: str) -> None:
        pass  # Placeholder for shape setting logic

    def set_size(self, width: int, height: int) -> None:
        if self.user_interface.current_image:
            self.user_interface.current_image = self.image_processor.resize(self.user_interface.current_image, width, height)
            self.user_interface.update_canvas(self.user_interface.current_image)

    def add_text(self, text: str, font: str, color: str) -> None:
        pass  # Placeholder for adding text logic

    def add_decorative_element(self, element: str) -> None:
        pass  # Placeholder for adding decorative elements logic

    def crop_image(self, x: int, y: int, width: int, height: int) -> None:
        if self.user_interface.current_image:
            self.user_interface.current_image = self.image_processor.crop(self.user_interface.current_image, x, y, width, height)
            self.user_interface.update_canvas(self.user_interface.current_image)

    def resize_image(self, new_width: int, new_height: int) -> None:
        self.set_size(new_width, new_height)

    def apply_effect(self, effect: str) -> None:
        if self.user_interface.current_image:
            self.user_interface.current_image = self.image_processor.apply_effect(self.user_interface.current_image, effect)
            self.user_interface.update_canvas(self.user_interface.current_image)

    def save_sticker(self, file_path: str) -> None:
        self.user_interface.save_sticker()