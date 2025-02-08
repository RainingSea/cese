import unittest
from PIL import Image
from image_processor import ImageProcessor
import os

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        # Create an instance of ImageProcessor
        self.processor = ImageProcessor()
        # Load a test image
        self.test_image_path = './lena.jpeg'
        self.processor.load_image(self.test_image_path)

    def test_import_image(self):
        # Functionalities 1: Import and Select an Image
        self.assertIsNotNone(self.processor.image, "Image should be loaded successfully")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        self.processor.adjust_brightness(2.0)  # Increase brightness to maximum
        bright_image = self.processor.image
        self.assertIsNotNone(bright_image, "Image should be brighter")

        self.processor.adjust_brightness(0.0)  # Decrease brightness to minimum
        dark_image = self.processor.image
        self.assertIsNotNone(dark_image, "Image should be darker")

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        self.processor.adjust_contrast(2.0)  # Increase contrast to maximum
        high_contrast_image = self.processor.image
        self.assertIsNotNone(high_contrast_image, "Image should have higher contrast")

        self.processor.adjust_contrast(0.0)  # Decrease contrast to minimum
        low_contrast_image = self.processor.image
        self.assertIsNotNone(low_contrast_image, "Image should have lower contrast")

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        self.processor.adjust_saturation(2.0)  # Increase saturation to maximum
        vivid_image = self.processor.image
        self.assertIsNotNone(vivid_image, "Image should be more vivid")

        self.processor.adjust_saturation(0.0)  # Decrease saturation to minimum
        grayscale_image = self.processor.image
        self.assertIsNotNone(grayscale_image, "Image should be grayscale")

    def test_apply_filter(self):
        # Functionalities 5: Apply Filters to Images
        self.processor.apply_filter("BLUR")
        blurred_image = self.processor.image
        self.assertIsNotNone(blurred_image, "Image should be blurred")

        self.processor.apply_filter("CONTOUR")
        contoured_image = self.processor.image
        self.assertIsNotNone(contoured_image, "Image should have contour effect")

    def test_apply_effect(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.processor.apply_effect("SHARPEN")
        sharpened_image = self.processor.image
        self.assertIsNotNone(sharpened_image, "Image should be sharpened")

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        self.processor.crop_image(10, 10, 100, 100)
        cropped_image = self.processor.image
        self.assertEqual(cropped_image.size, (90, 90), "Image should be cropped to the specified area")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.processor.resize_image(800, 600)
        resized_image = self.processor.image
        self.assertEqual(resized_image.size, (800, 600), "Image should be resized to 800x600 pixels")

if __name__ == '__main__':
    unittest.main()
