import unittest
from PIL import Image
import os
from image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        self.image_processor = ImageProcessor()
        self.test_image_path = './lena.jpeg'  # Ensure this image exists for testing
        self.output_image_path = './output_test_image.jpeg'

    def test_import_image(self):
        # Functionalities 1: Import and Select an Image
        try:
            self.image_processor.import_image(self.test_image_path)
            self.assertIsNotNone(self.image_processor.image)
        except Exception as e:
            self.fail(f"Import image failed with exception: {e}")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.adjust_brightness(2)  # Increase brightness
        self.assertIsNotNone(self.image_processor.image)

        self.image_processor.adjust_brightness(0)  # Decrease brightness
        self.assertIsNotNone(self.image_processor.image)

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.adjust_contrast(2)  # Increase contrast
        self.assertIsNotNone(self.image_processor.image)

        self.image_processor.adjust_contrast(0)  # Decrease contrast
        self.assertIsNotNone(self.image_processor.image)

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.adjust_saturation(2)  # Increase saturation
        self.assertIsNotNone(self.image_processor.image)

        self.image_processor.adjust_saturation(0)  # Decrease saturation
        self.assertIsNotNone(self.image_processor.image)

    def test_apply_filter(self):
        # Functionalities 5: Apply Filters to Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.apply_filter("BLUR")  # Apply blur filter
        self.assertIsNotNone(self.image_processor.image)

        self.image_processor.apply_filter("CONTOUR")  # Apply contour filter
        self.assertIsNotNone(self.image_processor.image)

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.crop(0, 0, 100, 100)  # Crop the image
        self.assertIsNotNone(self.image_processor.image)

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.image_processor.import_image(self.test_image_path)
        self.image_processor.resize(800, 600)  # Resize the image
        self.assertIsNotNone(self.image_processor.image)

    def tearDown(self):
        # Clean up the output image if it exists
        if os.path.exists(self.output_image_path):
            os.remove(self.output_image_path)

if __name__ == '__main__':
    unittest.main()
