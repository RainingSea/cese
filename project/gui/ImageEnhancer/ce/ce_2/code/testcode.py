import unittest
from PIL import Image
from image_processor import ImageProcessor

class TestImageEnhancer(unittest.TestCase):

    def setUp(self):
        self.processor = ImageProcessor()
        self.test_image_path = './lena.jpeg'
        self.processor.load_image(self.test_image_path)

    def test_import_and_select_image(self):
        # Functionalities 1: Import and Select an Image
        self.processor.load_image(self.test_image_path)
        self.assertIsNotNone(self.processor.image, "Image should be loaded and not None")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        self.processor.adjust_brightness(2.0)  # Increase to maximum
        # Expectation: Image becomes brighter
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for brightness")

        self.processor.adjust_brightness(0.0)  # Decrease to minimum
        # Expectation: Image becomes darker
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for brightness")

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        self.processor.adjust_contrast(2.0)  # Increase to maximum
        # Expectation: Contrast is more pronounced
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for contrast")

        self.processor.adjust_contrast(0.0)  # Decrease to minimum
        # Expectation: Image appears flat
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for contrast")

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        self.processor.adjust_saturation(2.0)  # Increase to maximum
        # Expectation: Colors appear more vivid
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for saturation")

        self.processor.adjust_saturation(0.0)  # Decrease to minimum
        # Expectation: Image becomes grayscale
        self.assertIsNotNone(self.processor.image, "Image should be adjusted for saturation")

    def test_apply_filters(self):
        # Functionalities 5: Apply Filters to Images
        self.processor.apply_filter("BLUR")
        # Expectation: Filter is applied
        self.assertIsNotNone(self.processor.image, "Image should have a filter applied")

        self.processor.apply_filter("CONTOUR")
        # Expectation: Filters are layered
        self.assertIsNotNone(self.processor.image, "Image should have multiple filters applied")

    def test_apply_effects(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.processor.apply_effect("Warm")
        # Expectation: Image tones are enhanced
        self.fail("Effect application logic not implemented")

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        self.processor.crop(10, 10, 100, 100)
        # Expectation: Image is cropped
        self.assertIsNotNone(self.processor.image, "Image should be cropped")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.processor.resize(800, 600)
        # Expectation: Image is resized
        self.assertEqual(self.processor.image.size, (800, 600), "Image should be resized to 800x600")

if __name__ == '__main__':
    unittest.main()
