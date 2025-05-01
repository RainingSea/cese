import unittest
from main import Main, ImageProcessor
from PIL import Image
import os

class TestImageEnhancer(unittest.TestCase):

    def setUp(self):
        self.image_processor = ImageProcessor()
        # Load a test image for testing purposes
        self.test_image_path = './lena.jpeg'  # Ensure this image is available in the specified path
        if not os.path.exists(self.test_image_path):
            self.fail("Test image not found at the specified path.")

        self.image_processor.load_image(self.test_image_path)

    def test_import_and_select_image(self):
        # Functionalities 1: Import and Select an Image
        self.assertIsNotNone(self.image_processor.image, "Image should load successfully.")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        original_image = self.image_processor.image.copy()
        self.image_processor.adjust_brightness(100)  # Increase brightness
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should be brighter.")
        
        self.image_processor.adjust_brightness(-100)  # Decrease brightness
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should be darker.")

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        original_image = self.image_processor.image.copy()
        self.image_processor.adjust_contrast(100)  # Increase contrast
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should have increased contrast.")
        
        self.image_processor.adjust_contrast(-100)  # Decrease contrast
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should have decreased contrast.")

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        original_image = self.image_processor.image.copy()
        self.image_processor.adjust_saturation(100)  # Increase saturation
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should have increased saturation.")
        
        self.image_processor.adjust_saturation(-100)  # Decrease saturation
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should have decreased saturation.")

    def test_apply_filters(self):
        # Functionalities 5: Apply Filters to Images
        self.fail("Filter application functionality not implemented.")

    def test_apply_effects(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.fail("Effects application functionality not implemented.")

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        original_image = self.image_processor.image.copy()
        self.image_processor.crop_image(0, 0, 100, 100)  # Crop the image
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should be cropped.")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        original_image = self.image_processor.image.copy()
        self.image_processor.resize_image(800, 600)  # Resize the image
        self.assertNotEqual(original_image.tobytes(), self.image_processor.image.tobytes(), "Image should be resized.")

if __name__ == '__main__':
    unittest.main()
