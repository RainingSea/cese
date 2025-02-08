import unittest
from brush import Brush
from canvas import Canvas
from color_palette import ColorPalette
from layer_manager import LayerManager
import tkinter as tk
from PIL import Image

class TestPaintPal(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.canvas = Canvas(self.root)
        self.layer_manager = LayerManager(self.root, self.canvas)
        self.color_palette = ColorPalette()
        self.brush = Brush(size=5, opacity=1.0, blend_mode='normal')
        self.canvas.set_brush(self.brush)

    def test_variety_of_brush_tools(self):
        # Functionalities 1: Offer a Variety of Brush Tools
        # Assuming different brush tools are represented by different sizes and blend modes
        self.brush.set_size(10)
        self.assertEqual(self.canvas.current_brush.size, 10)
        self.brush.set_blend_mode('multiply')
        self.assertEqual(self.canvas.current_brush.blend_mode, 'multiply')

    def test_selection_of_color_palettes(self):
        # Functionalities 2: Provide a Selection of Color Palettes
        self.color_palette.add_color('purple')
        self.assertIn('purple', self.color_palette.colors)
        self.color_palette.remove_color('purple')
        self.assertNotIn('purple', self.color_palette.colors)

    def test_layer_management_features(self):
        # Functionalities 3: Enable Layer Management Features
        initial_layer_count = len(self.layer_manager.layers)
        self.layer_manager.add_layer()
        self.assertEqual(len(self.layer_manager.layers), initial_layer_count + 1)
        self.layer_manager.delete_layer(0)
        self.assertEqual(len(self.layer_manager.layers), initial_layer_count)

    def test_adjust_brush_sizes(self):
        # Functionalities 4: Adjust Brush Sizes
        self.brush.set_size(15)
        self.assertEqual(self.canvas.current_brush.size, 15)
        self.brush.set_size(5)
        self.assertEqual(self.canvas.current_brush.size, 5)

    def test_adjust_brush_opacity(self):
        # Functionalities 5: Adjust Brush Opacity
        self.brush.set_opacity(0.5)
        self.assertEqual(self.canvas.current_brush.opacity, 0.5)

    def test_change_brush_blend_modes(self):
        # Functionalities 6: Change Brush Blend Modes
        self.brush.set_blend_mode('overlay')
        self.assertEqual(self.canvas.current_brush.blend_mode, 'overlay')

    def test_save_artwork(self):
        # Functionalities 7: Save Artwork Easily
        try:
            self.canvas.save_artwork('test_artwork.png')
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Saving artwork failed with exception: {e}")

    def test_export_artwork(self):
        # Functionalities 8: Export Artwork in Various File Formats
        try:
            self.canvas.save_artwork('test_artwork.jpeg')
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Exporting artwork failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
