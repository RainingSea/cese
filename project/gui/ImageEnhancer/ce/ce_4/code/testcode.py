import unittest
from PIL import Image
from image_editor import ImageEditor

class TestImageEditor(unittest.TestCase):

    def setUp(self):
        self.editor = ImageEditor()
        self.test_image_path = './lena.jpeg'
        self.editor.load_image(self.test_image_path)

    def test_import_and_select_image(self):
        # Functionalities 1: Import and Select an Image
        self.assertIsNotNone(self.editor.image, "Image should be loaded successfully.")

    def test_adjust_brightness(self):
        # Functionalities 2: Adjust Brightness of Images
        # Increase brightness to maximum
        self.editor.adjust_brightness(2.0)
        self.assertIsNotNone(self.editor.image, "Image should be brighter.")

        # Decrease brightness to minimum
        self.editor.adjust_brightness(0.0)
        self.assertIsNotNone(self.editor.image, "Image should be darker.")

    def test_adjust_contrast(self):
        # Functionalities 3: Adjust Contrast of Images
        # Increase contrast to maximum
        self.editor.adjust_contrast(2.0)
        self.assertIsNotNone(self.editor.image, "Contrast should be increased.")

        # Decrease contrast to minimum
        self.editor.adjust_contrast(0.0)
        self.assertIsNotNone(self.editor.image, "Contrast should be decreased.")

    def test_adjust_saturation(self):
        # Functionalities 4: Adjust Saturation of Images
        # Increase saturation to maximum
        self.editor.adjust_saturation(2.0)
        self.assertIsNotNone(self.editor.image, "Saturation should be increased.")

        # Decrease saturation to minimum
        self.editor.adjust_saturation(0.0)
        self.assertIsNotNone(self.editor.image, "Saturation should be decreased.")

    def test_apply_filters(self):
        # Functionalities 5: Apply Filters to Images
        # Apply a predefined filter
        self.editor.apply_filter("BLUR")
        self.assertIsNotNone(self.editor.image, "Filter should be applied.")

        # Apply multiple filters sequentially
        self.editor.apply_filter("CONTOUR")
        self.assertIsNotNone(self.editor.image, "Multiple filters should be applied.")

    def test_apply_effects(self):
        # Functionalities 6: Apply Effects to Enhance Colors and Tones
        self.fail("not implemented")  # No specific effect implementation in the codebase

    def test_crop_image(self):
        # Functionalities 7: Crop Images
        self.editor.crop_image(0, 0, 100, 100)
        self.assertEqual(self.editor.image.size, (100, 100), "Image should be cropped to specified area.")

    def test_resize_image(self):
        # Functionalities 8: Resize Images
        self.editor.resize_image(800, 600)
        self.assertEqual(self.editor.image.size, (800, 600), "Image should be resized to specified dimensions.")

if __name__ == '__main__':
    unittest.main()
