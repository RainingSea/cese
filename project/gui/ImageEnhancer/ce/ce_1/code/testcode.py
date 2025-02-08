import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from image_enhancer import ImageEnhancer
from gui import GUI

class TestImageEnhancer(unittest.TestCase):

    def setUp(self):
        self.image_enhancer = ImageEnhancer()
        self.gui = GUI()

    @patch('tkinter.filedialog.askopenfilename', return_value='./lena.jpeg')
    def test_import_image(self, mock_open):
        # Functionalities 1: Import and Select an Image
        self.gui.import_image()
        self.assertIsNotNone(self.image_enhancer.original_image)
        self.assertIsNotNone(self.image_enhancer.edited_image)

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        self.image_enhancer.original_image = Image.new('RGB', (100, 100), color='white')
        self.image_enhancer.edited_image = self.image_enhancer.original_image.copy()

        # Increase brightness to maximum
        self.image_enhancer.adjust_brightness(2.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

        # Decrease brightness to minimum
        self.image_enhancer.adjust_brightness(0.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        self.image_enhancer.original_image = Image.new('RGB', (100, 100), color='gray')
        self.image_enhancer.edited_image = self.image_enhancer.original_image.copy()

        # Increase contrast to maximum
        self.image_enhancer.adjust_contrast(2.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

        # Decrease contrast to minimum
        self.image_enhancer.adjust_contrast(0.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        self.image_enhancer.original_image = Image.new('RGB', (100, 100), color='blue')
        self.image_enhancer.edited_image = self.image_enhancer.original_image.copy()

        # Increase saturation to maximum
        self.image_enhancer.adjust_saturation(2.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

        # Decrease saturation to minimum
        self.image_enhancer.adjust_saturation(0.0)
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

    def test_apply_filters(self):
        # Functionalities 5: Apply Filters to Images
        self.image_enhancer.original_image = Image.new('RGB', (100, 100), color='green')
        self.image_enhancer.edited_image = self.image_enhancer.original_image.copy()

        # Apply Sepia filter
        self.image_enhancer.apply_effect("SEPIA")
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

        # Apply multiple filters
        self.image_enhancer.apply_filter("BLUR")
        self.assertNotEqual(self.image_enhancer.original_image, self.image_enhancer.edited_image)

    def test_apply_effects(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.fail("not implemented")

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        self.fail("not implemented")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
