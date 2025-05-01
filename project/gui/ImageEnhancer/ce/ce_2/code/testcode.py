import unittest
from image_processor import ImageProcessor
from PIL import Image
import os

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        self.image_processor = ImageProcessor()
        self.test_image_path = './lena.jpeg'  # Ensure this image exists in the specified path
        self.invalid_image_path = './invalid_image.jpeg'

    def test_import_and_select_image(self):
        # Functionalities 1: Import and Select an Image
        try:
            self.image_processor.load_image(self.test_image_path)
            self.assertIsInstance(self.image_processor.image, Image.Image)
        except Exception as e:
            self.fail(f"Image import failed with exception: {e}")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        self.image_processor.load_image(self.test_image_path)
        original_image = self.image_processor.image.copy()
        
        # Increase brightness
        self.image_processor.adjust_brightness(100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

        # Decrease brightness
        self.image_processor.adjust_brightness(-100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        self.image_processor.load_image(self.test_image_path)
        original_image = self.image_processor.image.copy()

        # Increase contrast
        self.image_processor.adjust_contrast(100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

        # Decrease contrast
        self.image_processor.adjust_contrast(-100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        self.image_processor.load_image(self.test_image_path)
        original_image = self.image_processor.image.copy()

        # Increase saturation
        self.image_processor.adjust_saturation(100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

        # Decrease saturation
        self.image_processor.adjust_saturation(-100)
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes())

    def test_apply_filters(self):
        # Functionalities 5: Apply Filters to Images
        self.fail("not implemented")  # Placeholder for filter functionality

    def test_apply_effects(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.fail("not implemented")  # Placeholder for effects functionality

    def test_crop_images(self):
        # Functionalities 7: Crop Images
        self.image_processor.load_image(self.test_image_path)
        original_size = self.image_processor.image.size
        
        # Crop the image
        self.image_processor.crop_image(0, 0, original_size[0] // 2, original_size[1] // 2)
        self.assertNotEqual(original_size, self.image_processor.image.size)

    def test_resize_images(self):
        # Functionalities 8: Resize Images
        self.image_processor.load_image(self.test_image_path)
        original_size = self.image_processor.image.size
        
        # Resize the image
        self.image_processor.resize_image(800, 600)
        self.assertEqual(self.image_processor.image.size, (800, 600))

if __name__ == '__main__':
    unittest.main()
