import unittest
from brush import Brush
from layer import LayerManager, Layer
from palette import Color, ColorPalette
from main import Main
import tkinter as tk

class TestPaintPal(unittest.TestCase):

    def setUp(self):
        # Set up the main application for testing
        self.root = tk.Tk()
        self.app = Main(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_brush_tools(self):
        # Functionalities 1: Offer a Variety of Brush Tools
        # Since the code does not implement different brush tools, this test will fail
        self.fail("Brush tool selection not implemented")

    def test_color_palette(self):
        # Functionalities 2: Provide a Selection of Color Palettes
        palette = ColorPalette()
        red = Color(name="Red", hex_value="#FF0000")
        palette.add_color(red)
        self.assertIn(red, palette.colors, "Color not added to palette")

        # Test custom color creation
        custom_color = Color(name="Custom", hex_value="#123456")
        palette.add_color(custom_color)
        self.assertIn(custom_color, palette.colors, "Custom color not saved in palette")

    def test_layer_management(self):
        # Functionalities 3: Enable Layer Management Features
        layer_manager = self.app.layer_manager
        initial_layer_count = len(layer_manager.get_layers())

        # Add a new layer
        new_layer = layer_manager.create_layer("Layer 1")
        self.assertIn(new_layer, layer_manager.get_layers(), "New layer not created")

        # Delete the layer
        layer_manager.delete_layer(new_layer)
        self.assertNotIn(new_layer, layer_manager.get_layers(), "Layer not deleted")

        # Reordering layers is not implemented, so this will fail
        self.fail("Layer reordering not implemented")

    def test_brush_size_adjustment(self):
        # Functionalities 4: Adjust Brush Sizes
        brush = self.app.current_brush
        initial_size = brush.size
        brush.set_size(10.0)
        self.assertEqual(brush.size, 10.0, "Brush size not increased")

        brush.set_size(3.0)
        self.assertEqual(brush.size, 3.0, "Brush size not decreased")

    def test_brush_opacity_adjustment(self):
        # Functionalities 5: Adjust Brush Opacity
        brush = self.app.current_brush
        brush.set_opacity(0.5)
        self.assertEqual(brush.opacity, 0.5, "Brush opacity not adjusted")

    def test_blend_modes(self):
        # Functionalities 6: Change Brush Blend Modes
        # Since blend modes are not implemented, this test will fail
        self.fail("Brush blend modes not implemented")

    def test_save_artwork(self):
        # Functionalities 7: Save Artwork Easily
        result = self.app.save_artwork("test_artwork")
        self.assertTrue(result, "Artwork not saved successfully")

    def test_export_artwork(self):
        # Functionalities 8: Export Artwork in Various File Formats
        # Since export functionality is not implemented, this test will fail
        self.fail("Artwork export not implemented")

if __name__ == '__main__':
    unittest.main()
