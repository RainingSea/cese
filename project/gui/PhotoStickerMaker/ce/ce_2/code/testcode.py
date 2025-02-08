import unittest
from photo_editor import PhotoEditor
from PIL import Image
import os

class TestPhotoStickerMaker(unittest.TestCase):

    def setUp(self):
        self.photo_editor = PhotoEditor()
        self.test_image_path = "/Users/liujie/Desktop/SD-bench/testdata/testcase.png"
        self.output_image_path = "/Users/liujie/Desktop/SD-bench/testdata/output.png"

    def test_import_photo(self):
        # Functionalities 1: Import and Select a Photo
        try:
            self.photo_editor.import_photo(self.test_image_path)
            self.assertEqual(self.photo_editor.image_path, self.test_image_path)
        except FileNotFoundError:
            self.fail("FileNotFoundError raised unexpectedly!")

    def test_choose_shape(self):
        # Functionalities 2: Choose the Shape of the Sticker
        self.photo_editor.choose_shape("circle")
        self.assertEqual(self.photo_editor.shape, "circle")

    def test_set_size(self):
        # Functionalities 3: Set the Size of the Sticker
        self.photo_editor.set_size(200, 200)
        self.assertEqual(self.photo_editor.size, (200, 200))

    def test_add_text(self):
        # Functionalities 4: Add Text to the Sticker
        self.photo_editor.add_text("Hello", "Arial", "black")
        self.assertEqual(self.photo_editor.text, ("Hello", "Arial", "black"))

    def test_add_decorative_element(self):
        # Functionalities 5: Add Decorative Elements to the Sticker
        self.fail("not implemented")

    def test_crop_image(self):
        # Functionalities 6: Crop the Photo
        self.photo_editor.import_photo(self.test_image_path)
        self.photo_editor.crop_image(0, 0, 50, 50)
        cropped_image = self.photo_editor.image_path
        self.assertIsInstance(cropped_image, Image.Image)

    def test_resize_image(self):
        # Functionalities 7: Resize the Photo
        self.photo_editor.import_photo(self.test_image_path)
        self.photo_editor.resize_image(150, 150)
        resized_image = self.photo_editor.image_path
        self.assertIsInstance(resized_image, Image.Image)

    def test_apply_effect(self):
        # Functionalities 8: Apply Effects to the Photo
        self.photo_editor.import_photo(self.test_image_path)
        self.photo_editor.apply_effect("grayscale")
        effect_image = self.photo_editor.image_path
        self.assertIsInstance(effect_image, Image.Image)

    def test_save_as_png(self):
        # Functionalities 9: Save the Sticker as a Transparent PNG File
        self.photo_editor.import_photo(self.test_image_path)
        self.photo_editor.save_as_png(self.output_image_path)
        self.assertTrue(os.path.exists(self.output_image_path))
        os.remove(self.output_image_path)

if __name__ == '__main__':
    unittest.main()
