import unittest
from brush import Brush
from canvas import Canvas
from layer_manager import LayerManager
from toolbar import Toolbar

class TestPaintPal(unittest.TestCase):

    def setUp(self):
        self.toolbar = Toolbar()
        self.canvas = Canvas()
        self.layer_manager = LayerManager()

    def test_variety_of_brush_tools(self):
        # Functionalities 1: Offer a Variety of Brush Tools
        # Test selecting different brush tools
        round_brush = Brush(size=5, opacity=1.0, blend_mode='normal')
        textured_brush = Brush(size=10, opacity=0.8, blend_mode='multiply')
        
        self.toolbar.select_brush(round_brush)
        self.assertEqual(self.toolbar.selected_brush.size, 5)
        self.assertEqual(self.toolbar.selected_brush.opacity, 1.0)
        self.assertEqual(self.toolbar.selected_brush.blend_mode, 'normal')
        
        self.toolbar.select_brush(textured_brush)
        self.assertEqual(self.toolbar.selected_brush.size, 10)
        self.assertEqual(self.toolbar.selected_brush.opacity, 0.8)
        self.assertEqual(self.toolbar.selected_brush.blend_mode, 'multiply')

    def test_selection_of_color_palettes(self):
        # Functionalities 2: Provide a Selection of Color Palettes
        self.fail("not implemented")  # No implementation for color palettes in the codebase

    def test_layer_management_features(self):
        # Functionalities 3: Enable Layer Management Features
        # Test adding a new layer
        new_layer = self.layer_manager.create_layer()
        self.assertIn(new_layer, self.layer_manager.layers)

        # Test deleting an existing layer
        self.layer_manager.delete_layer(new_layer)
        self.assertNotIn(new_layer, self.layer_manager.layers)

        # Test reordering layers (not implemented)
        self.fail("reordering layers not implemented")

    def test_adjust_brush_sizes(self):
        # Functionalities 4: Adjust Brush Sizes
        self.toolbar.adjust_brush_size(15)
        self.assertEqual(self.toolbar.selected_brush.size, 15)
        self.toolbar.adjust_brush_size(3)
        self.assertEqual(self.toolbar.selected_brush.size, 3)

    def test_adjust_brush_opacity(self):
        # Functionalities 5: Adjust Brush Opacity
        self.toolbar.adjust_brush_opacity(0.5)
        self.assertEqual(self.toolbar.selected_brush.opacity, 0.5)

    def test_change_brush_blend_modes(self):
        # Functionalities 6: Change Brush Blend Modes
        self.toolbar.change_blend_mode('overlay')
        self.assertEqual(self.toolbar.selected_brush.blend_mode, 'overlay')

    def test_save_artwork(self):
        # Functionalities 7: Save Artwork Easily
        self.fail("saving artwork not implemented")  # No implementation for saving artwork in the codebase

    def test_export_artwork(self):
        # Functionalities 8: Export Artwork in Various File Formats
        self.fail("exporting artwork not implemented")  # No implementation for exporting artwork in the codebase

if __name__ == '__main__':
    unittest.main()
