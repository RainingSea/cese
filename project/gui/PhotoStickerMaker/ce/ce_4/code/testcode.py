import unittest
from tkinter import Tk
from PIL import Image
from main import PhotoStickerMaker

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = PhotoStickerMaker()
        self.app.root.update()  # Update the GUI

    def tearDown(self):
        # Destroy the application after each test
        self.app.root.destroy()

    def test_import_photo(self):
        # Functionalities 1: Import and Select a Photo
        # Simulate importing a photo
        test_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.app.photo = Image.open(test_image_path)
        self.app.display_photo()
        self.assertIsNotNone(self.app.photo, "The photo should be loaded successfully.")
        self.assertIsNotNone(self.app.tk_image, "The photo should be displayed in the application.")

    def test_choose_shape(self):
        # Functionalities 2: Choose the Shape of the Sticker
        self.app.select_shape("Circle")
        self.assertEqual(self.app.selected_shape.get(), "Circle", "The selected shape should be 'Circle'.")

    def test_set_size(self):
        # Functionalities 3: Set the Size of the Sticker
        self.app.photo = Image.new("RGB", (100, 100))
        self.app.set_size(200, 200)
        self.assertEqual(self.app.photo.size, (200, 200), "The photo size should be updated to (200, 200).")

    def test_add_text(self):
        # Functionalities 4: Add Text to the Sticker
        self.app.photo = Image.new("RGB", (100, 100))
        self.app.text_input.insert(0, "Hello")
        self.app.add_text()
        # Since we can't visually check the text, we assume success if no errors occur

    def test_add_decorative_element(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.fail("not implemented")  # Placeholder as the functionality is not implemented

    def test_crop_photo(self):
        # Functionalities 6: Crop the Photo
        self.app.photo = Image.new("RGB", (300, 300))
        self.app.crop_photo(50, 50, 100, 100)
        self.assertEqual(self.app.photo.size, (100, 100), "The photo should be cropped to (100, 100).")

    def test_resize_photo(self):
        # Functionalities 7: Resize the Photo
        self.app.photo = Image.new("RGB", (300, 300))
        self.app.resize_photo(150, 150)
        self.assertEqual(self.app.photo.size, (150, 150), "The photo should be resized to (150, 150).")

    def test_apply_effect(self):
        # Functionalities 8: Apply Effects to the Photo
        self.app.photo = Image.new("RGB", (100, 100))
        self.app.apply_effect("BLUR")
        # Since we can't visually check the effect, we assume success if no errors occur

    def test_save_sticker(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.app.photo = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
        self.app.save_sticker("test_sticker.png")
        self.assertTrue(os.path.exists("stickers/test_sticker.png"), "The sticker should be saved successfully.")

if __name__ == '__main__':
    unittest.main()
