import unittest
from PIL import Image as PILImage
from Image import Image as CustomImage
from main import ImageEnhancer
import os

class TestImageEnhancer(unittest.TestCase):

    def setUp(self):
        self.image_enhancer = ImageEnhancer()
        self.test_image_path = './lena.jpeg'  # Ensure this path is correct and the file exists
        self.image_enhancer.import_image(self.test_image_path)

    def test_import_image(self):
        # Functionalities 1: Import and Select an Image
        self.assertIsNotNone(self.image_enhancer.image, "Image should be loaded")
        self.assertEqual(self.image_enhancer.image_path, self.test_image_path, "Image path should be set correctly")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        original_image = self.image_enhancer.image.image.copy()
        self.image_enhancer.adjust_brightness(2.0)  # Increase brightness to maximum
        bright_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, bright_image, "Image should be brighter")

        self.image_enhancer.adjust_brightness(0.0)  # Decrease brightness to minimum
        dark_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, dark_image, "Image should be darker")

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        original_image = self.image_enhancer.image.image.copy()
        self.image_enhancer.adjust_contrast(2.0)  # Increase contrast to maximum
        high_contrast_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, high_contrast_image, "Image should have higher contrast")

        self.image_enhancer.adjust_contrast(0.0)  # Decrease contrast to minimum
        low_contrast_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, low_contrast_image, "Image should have lower contrast")

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        original_image = self.image_enhancer.image.image.copy()
        self.image_enhancer.adjust_saturation(2.0)  # Increase saturation to maximum
        saturated_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, saturated_image, "Image should be more saturated")

        self.image_enhancer.adjust_saturation(0.0)  # Decrease saturation to minimum
        grayscale_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, grayscale_image, "Image should be grayscale")

    def test_apply_filter(self):
        # Functionalities 5: Apply Filters to Images
        original_image = self.image_enhancer.image.image.copy()
        self.image_enhancer.apply_filter("BLUR")
        blurred_image = self.image_enhancer.image.image
        self.assertNotEqual(original_image, blurred_image, "Image should be blurred")

        self.image_enhancer.apply_filter("CONTOUR")
        contoured_image = self.image_enhancer.image.image
        self.assertNotEqual(blurred_image, contoured_image, "Image should have contour filter applied")

    def test_apply_effect(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.fail("not implemented")  # Placeholder as the functionality is not implemented

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        original_size = self.image_enhancer.image.image.size
        self.image_enhancer.crop_image(10, 10, 100, 100)
        cropped_size = self.image_enhancer.image.image.size
        self.assertNotEqual(original_size, cropped_size, "Image should be cropped")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.image_enhancer.resize_image(800, 600)
        resized_size = self.image_enhancer.image.image.size
        self.assertEqual(resized_size, (800, 600), "Image should be resized to 800x600")

if __name__ == '__main__':
    unittest.main()
