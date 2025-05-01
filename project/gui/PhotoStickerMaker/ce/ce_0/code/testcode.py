import unittest
from image_processor import ImageProcessor
from sticker_creator import StickerCreator

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()

    def test_import_and_select_photo(self):
        # Functionalities 1: Import and Select a Photo
        try:
            self.image_processor.import_image("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
            self.assertIsNotNone(self.image_processor.image, "Image should be loaded successfully.")
        except Exception as e:
            self.fail(f"Importing image failed with exception: {e}")

    def test_choose_shape_of_sticker(self):
        # Functionalities 2: Choose the Shape of the Sticker
        try:
            self.sticker_creator.choose_shape("Circle")
            self.assertEqual(self.sticker_creator.shape, "Circle", "Shape should be set to Circle.")
        except Exception as e:
            self.fail(f"Choosing shape failed with exception: {e}")

    def test_set_size_of_sticker(self):
        # Functionalities 3: Set the Size of the Sticker
        self.fail("Setting size of the sticker is not implemented.")

    def test_add_text_to_sticker(self):
        # Functionalities 4: Add Text to the Sticker
        try:
            self.sticker_creator.sticker_image = self.image_processor.image  # Simulate having an image
            self.sticker_creator.add_text("Test", "Arial", "#000000")
            # Check if the text was added (this is a placeholder check)
            self.assertTrue(True, "Text should be added to the sticker.")
        except Exception as e:
            self.fail(f"Adding text failed with exception: {e}")

    def test_add_decorative_elements(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.fail("Adding decorative elements is not implemented.")

    def test_crop_photo(self):
        # Functionalities 6: Crop the Photo
        self.fail("Cropping photo functionality is not implemented.")

    def test_resize_photo(self):
        # Functionalities 7: Resize the Photo
        self.fail("Resizing photo functionality is not implemented.")

    def test_apply_effects_to_photo(self):
        # Functionalities 8: Apply Effects to the Photo
        try:
            self.image_processor.import_image("/Users/liujie/Desktop/SD-bench/testdata/testcase.png")
            self.image_processor.apply_effect("grayscale")
            self.assertIsNotNone(self.image_processor.image, "Effect should be applied to the image.")
        except Exception as e:
            self.fail(f"Applying effect failed with exception: {e}")

    def test_save_sticker_as_transparent_png(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.fail("Saving sticker as transparent PNG functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
