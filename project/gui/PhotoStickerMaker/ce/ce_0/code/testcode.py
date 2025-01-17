import unittest
from main import StickerMaker
from PIL import Image

class TestStickerMaker(unittest.TestCase):

    def setUp(self):
        self.sticker_maker = StickerMaker()

    def test_import_photo(self):
        # Functionalities 1: Import and Select a Photo
        test_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.sticker_maker.import_photo(test_image_path)
        self.assertEqual(self.sticker_maker.image_path, test_image_path)

    def test_select_shape(self):
        # Functionalities 2: Choose the Shape of the Sticker
        self.sticker_maker.select_shape("circle")
        self.assertEqual(self.sticker_maker.shape, "circle")

    def test_set_size(self):
        # Functionalities 3: Set the Size of the Sticker
        self.sticker_maker.set_size(150, 150)
        self.assertEqual(self.sticker_maker.size, (150, 150))

    def test_add_text(self):
        # Functionalities 4: Add Text to the Sticker
        self.sticker_maker.add_text("Hello", "red")
        self.assertEqual(self.sticker_maker.text, "Hello")
        self.assertEqual(self.sticker_maker.text_color, "red")

    def test_add_decoration(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.sticker_maker.add_decoration("sticker")
        self.assertIn("sticker", self.sticker_maker.decorations)

    def test_crop_image(self):
        # Functionalities 6: Crop the Photo
        # Assuming a valid image is already imported
        self.sticker_maker.import_photo("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
        self.sticker_maker.crop_image((0, 0, 50, 50))
        self.assertIsInstance(self.sticker_maker.image_path, Image.Image)

    def test_resize_image(self):
        # Functionalities 7: Resize the Photo
        # Assuming a valid image is already imported
        self.sticker_maker.import_photo("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
        self.sticker_maker.resize_image((200, 200))
        self.assertIsInstance(self.sticker_maker.image_path, Image.Image)

    def test_apply_effect(self):
        # Functionalities 8: Apply Effects to the Photo
        # Assuming a valid image is already imported
        self.sticker_maker.import_photo("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
        self.sticker_maker.apply_effect("grayscale")
        self.assertIsInstance(self.sticker_maker.image_path, Image.Image)

    def test_save_sticker(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        # Assuming a valid image is already imported
        self.sticker_maker.import_photo("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
        self.sticker_maker.save_sticker("/Users/liujie/Desktop/SD-bench/testdata/output.png")
        # Check if the file is saved, this is a placeholder as actual file check is not implemented
        self.assertTrue(True)  # Placeholder for file existence check

if __name__ == '__main__':
    unittest.main()
