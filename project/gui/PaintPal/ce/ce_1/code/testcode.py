import unittest
from brush import Brush
from color_palette import ColorPalette
from layer_manager import LayerManager
from canvas import Canvas
from toolbar import Toolbar
import os

class TestPaintPal(unittest.TestCase):

    def setUp(self):
        self.toolbar = Toolbar()
        self.color_palette = ColorPalette()
        self.layer_manager = LayerManager()
        self.canvas = Canvas()

    def test_variety_of_brush_tools(self):
        # Functionalities 1: Offer a Variety of Brush Tools
        initial_brush = self.toolbar.brushes[0]
        self.toolbar.select_brush(self.toolbar.brushes[1])
        self.assertNotEqual(initial_brush, self.toolbar.current_brush, "Brush tool selection failed.")

    def test_selection_of_color_palettes(self):
        # Functionalities 2: Provide a Selection of Color Palettes
        initial_color_count = len(self.color_palette.colors)
        self.color_palette.select_color("red")
        self.assertIn("red", self.color_palette.colors, "Color selection failed.")
        self.assertEqual(len(self.color_palette.colors), initial_color_count + 1, "Color not added to palette.")

        # Attempt to create a custom color
        self.color_palette.select_color("custom_color")
        self.assertIn("custom_color", self.color_palette.colors, "Custom color creation failed.")

    def test_layer_management_features(self):
        # Functionalities 3: Enable Layer Management Features
        initial_layer_count = len(self.layer_manager.get_layers())
        self.layer_manager.add_layer()
        self.assertEqual(len(self.layer_manager.get_layers()), initial_layer_count + 1, "Layer addition failed.")

        self.layer_manager.delete_layer(0)
        self.assertEqual(len(self.layer_manager.get_layers()), initial_layer_count, "Layer deletion failed.")

        # Reorder layers is not implemented in the codebase
        self.fail("Reorder layers functionality not implemented.")

    def test_adjust_brush_sizes(self):
        # Functionalities 4: Adjust Brush Sizes
        initial_size = self.toolbar.current_brush.size
        self.toolbar.adjust_size(10)
        self.assertEqual(self.toolbar.current_brush.size, 10, "Brush size adjustment failed.")
        self.toolbar.adjust_size(initial_size)
        self.assertEqual(self.toolbar.current_brush.size, initial_size, "Brush size reset failed.")

    def test_adjust_brush_opacity(self):
        # Functionalities 5: Adjust Brush Opacity
        self.toolbar.adjust_opacity(0.5)
        self.assertEqual(self.toolbar.current_brush.opacity, 0.5, "Brush opacity adjustment failed.")

    def test_change_brush_blend_modes(self):
        # Functionalities 6: Change Brush Blend Modes
        initial_blend_mode = self.toolbar.current_brush.blend_mode
        self.toolbar.change_blend_mode("multiply")
        self.assertEqual(self.toolbar.current_brush.blend_mode, "multiply", "Blend mode change failed.")
        self.toolbar.change_blend_mode(initial_blend_mode)

    def test_save_artwork(self):
        # Functionalities 7: Save Artwork Easily
        filename = "test_artwork.png"
        self.canvas.save_artwork(filename)
        self.assertTrue(os.path.exists(filename), "Artwork saving failed.")
        os.remove(filename)

    def test_export_artwork(self):
        # Functionalities 8: Export Artwork in Various File Formats
        filename = "test_export.png"
        self.canvas.save_artwork(filename)
        self.assertTrue(os.path.exists(filename), "Artwork export failed.")
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
