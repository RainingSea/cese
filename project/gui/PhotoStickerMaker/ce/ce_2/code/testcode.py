import unittest
from main import Main, ImageProcessor, StickerCreator, Shape, Text
from PIL import Image

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        self.main_app = Main()
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()
        self.shape = Shape()
        self.text = Text()
        # Load a test image for testing
        self.test_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.image = Image.open(self.test_image_path)

    def test_import_and_select_photo(self):
        # Functionalities 1: Import and Select a Photo
        self.main_app.import_photo()  # Simulate importing a photo
        # Check if the image is loaded and displayed
        self.assertIsNotNone(self.main_app.image, "Image should be loaded successfully.")

    def test_choose_shape_of_sticker(self):
        # Functionalities 2: Choose the Shape of the Sticker
        shape_image = self.shape.select_shape("Circle")
        self.assertIsNotNone(shape_image, "Shape should be applied to the image.")

    def test_set_size_of_sticker(self):
        # Functionalities 3: Set the Size of the Sticker
        self.fail("Size adjustment functionality not implemented.")

    def test_add_text_to_sticker(self):
        # Functionalities 4: Add Text to the Sticker
        modified_image = self.text.add_text(self.image.copy(), "Sample Text", "Arial", "black")
        self.assertIsNotNone(modified_image, "Text should be added to the sticker.")

    def test_add_decorative_elements_to_sticker(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.fail("Decorative elements functionality not implemented.")

    def test_crop_photo(self):
        # Functionalities 6: Crop the Photo
        cropped_image = self.image_processor.crop(self.image, (0, 0, 100, 100))
        self.assertEqual(cropped_image.size, (100, 100), "Image should be cropped to the selected portion.")

    def test_resize_photo(self):
        # Functionalities 7: Resize the Photo
        resized_image = self.image_processor.resize(self.image, (200, 200))
        self.assertEqual(resized_image.size, (200, 200), "Image dimensions should be updated without distortion.")

    def test_apply_effects_to_photo(self):
        # Functionalities 8: Apply Effects to the Photo
        grayscale_image = self.image_processor.apply_effect(self.image, "grayscale")
        self.assertEqual(grayscale_image.mode, "L", "Effect should be applied to the image.")
        # Test applying multiple effects
        self.fail("Multiple effects application functionality not implemented.")

    def test_save_sticker_as_png(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.fail("Saving sticker functionality not implemented.")

if __name__ == '__main__':
    unittest.main()
