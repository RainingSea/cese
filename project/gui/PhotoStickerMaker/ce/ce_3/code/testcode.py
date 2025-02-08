import unittest
from PIL import Image
from main import ImageProcessor, StickerDesigner, Main
from effects import Effects
import os

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        # Initialize the main application and load a sample image
        self.app = Main()
        self.sample_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.sample_image = Image.open(self.sample_image_path)

    def test_import_and_select_photo(self):
        # Functionalities 1: Import and Select a Photo
        try:
            self.app.display_image(self.sample_image)
            self.assertIsNotNone(self.app.tk_image)
        except Exception as e:
            self.fail(f"Import and Select a Photo failed: {e}")

    def test_choose_shape_of_sticker(self):
        # Functionalities 2: Choose the Shape of the Sticker
        sticker_designer = StickerDesigner()
        shape = sticker_designer.select_shape("circle")
        self.assertEqual(shape["type"], "circle")

    def test_set_size_of_sticker(self):
        # Functionalities 3: Set the Size of the Sticker
        sticker_designer = StickerDesigner()
        sticker_designer.set_size((150, 150))
        self.assertEqual(sticker_designer.size, (150, 150))

    def test_add_text_to_sticker(self):
        # Functionalities 4: Add Text to the Sticker
        sticker_designer = StickerDesigner()
        sticker_designer.add_text("Hello", "Arial", "black")
        self.assertIn({"text": "Hello", "font": "Arial", "color": "black"}, sticker_designer.text_elements)

    def test_add_decorative_elements_to_sticker(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        # Since the functionality is not implemented, this test will fail
        self.fail("Add Decorative Elements to the Sticker not implemented")

    def test_crop_photo(self):
        # Functionalities 6: Crop the Photo
        image_processor = ImageProcessor()
        cropped_image = image_processor.crop_image(self.sample_image, (0, 0, 100, 100))
        self.assertEqual(cropped_image.size, (100, 100))

    def test_resize_photo(self):
        # Functionalities 7: Resize the Photo
        image_processor = ImageProcessor()
        resized_image = image_processor.resize_image(self.sample_image, (200, 200))
        self.assertEqual(resized_image.size, (200, 200))

    def test_apply_effects_to_photo(self):
        # Functionalities 8: Apply Effects to the Photo
        image_processor = ImageProcessor()
        blurred_image = image_processor.apply_effect(self.sample_image, "blur")
        sharpened_image = image_processor.apply_effect(blurred_image, "sharpen")
        self.assertIsNotNone(sharpened_image)

    def test_save_sticker_as_transparent_png(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.app.save_sticker()
        self.assertTrue(os.path.exists("sticker.png"))
        saved_image = Image.open("sticker.png")
        self.assertEqual(saved_image.mode, "RGBA")
        os.remove("sticker.png")

if __name__ == '__main__':
    unittest.main()
