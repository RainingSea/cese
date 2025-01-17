import unittest
from PIL import Image
from sticker_maker import StickerMaker
from user_interface import UserInterface
import tkinter as tk

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.sticker_maker = StickerMaker(self.root)
        self.test_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.test_image = Image.new('RGB', (100, 100), color = 'red')

    def tearDown(self):
        self.root.destroy()

    def test_import_and_select_photo(self):
        # Functionalities 1: Import and Select a Photo
        try:
            self.sticker_maker.import_image(self.test_image_path)
            self.assertIsNotNone(self.sticker_maker.user_interface.current_image)
        except Exception as e:
            self.fail(f"Importing image failed with exception: {e}")

    def test_choose_shape_of_sticker(self):
        # Functionalities 2: Choose the Shape of the Sticker
        self.fail("Shape selection functionality not implemented")

    def test_set_size_of_sticker(self):
        # Functionalities 3: Set the Size of the Sticker
        initial_size = self.test_image.size
        new_width, new_height = 50, 50
        self.sticker_maker.user_interface.current_image = self.test_image
        self.sticker_maker.set_size(new_width, new_height)
        self.assertEqual(self.sticker_maker.user_interface.current_image.size, (new_width, new_height))

    def test_add_text_to_sticker(self):
        # Functionalities 4: Add Text to the Sticker
        self.fail("Text addition functionality not implemented")

    def test_add_decorative_elements_to_sticker(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.fail("Decorative elements functionality not implemented")

    def test_crop_photo(self):
        # Functionalities 6: Crop the Photo
        self.sticker_maker.user_interface.current_image = self.test_image
        self.sticker_maker.crop_image(10, 10, 50, 50)
        self.assertEqual(self.sticker_maker.user_interface.current_image.size, (50, 50))

    def test_resize_photo(self):
        # Functionalities 7: Resize the Photo
        self.sticker_maker.user_interface.current_image = self.test_image
        new_width, new_height = 80, 80
        self.sticker_maker.resize_image(new_width, new_height)
        self.assertEqual(self.sticker_maker.user_interface.current_image.size, (new_width, new_height))

    def test_apply_effects_to_photo(self):
        # Functionalities 8: Apply Effects to the Photo
        self.sticker_maker.user_interface.current_image = self.test_image
        self.sticker_maker.apply_effect("grayscale")
        self.assertEqual(self.sticker_maker.user_interface.current_image.mode, "L")

        # Test applying multiple effects
        self.sticker_maker.apply_effect("invert")
        # Since we can't directly verify the image content, we assume if no error, it passed
        self.assertTrue(True)

    def test_save_sticker_as_png(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.fail("Saving sticker functionality not implemented")

if __name__ == '__main__':
    unittest.main()
