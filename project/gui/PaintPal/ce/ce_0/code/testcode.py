import unittest
from tkinter import Tk
from canvas import Canvas
from toolbar import Toolbar
from layer_manager import LayerManager
from brush import Brush

class TestPaintPal(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.canvas = Canvas(self.root)
        self.toolbar = Toolbar(self.root, self.canvas)
        self.layer_manager = LayerManager(self.root)

    def test_brush_tools(self):
        # Functionalities 1: Offer a Variety of Brush Tools
        self.toolbar.select_brush(Brush(size=10, opacity=1.0, blend_mode="normal"))
        self.assertEqual(self.canvas.current_brush.size, 10)
        self.assertEqual(self.canvas.current_brush.opacity, 1.0)
        self.assertEqual(self.canvas.current_brush.blend_mode, "normal")

    def test_color_palette_selection(self):
        # Functionalities 2: Provide a Selection of Color Palettes
        self.canvas.current_color = "red"
        self.assertEqual(self.canvas.current_color, "red")

        # Attempt to create a custom color (not implemented)
        self.fail("Custom color creation not implemented")

    def test_layer_management(self):
        # Functionalities 3: Enable Layer Management Features
        self.layer_manager.create_layer()
        self.assertEqual(len(self.layer_manager.layers), 1)

        self.layer_manager.delete_layer(0)
        self.assertEqual(len(self.layer_manager.layers), 0)

        # Reordering layers (not implemented)
        self.fail("Layer reordering not implemented")

    def test_adjust_brush_size(self):
        # Functionalities 4: Adjust Brush Sizes
        self.toolbar.brush_size_slider.set(20)
        self.toolbar.adjust_size(20)
        self.assertEqual(self.toolbar.current_brush.size, 20)

    def test_adjust_brush_opacity(self):
        # Functionalities 5: Adjust Brush Opacity
        self.toolbar.opacity_slider.set(0.5)
        self.toolbar.adjust_opacity(0.5)
        self.assertEqual(self.toolbar.current_brush.opacity, 0.5)

    def test_change_blend_mode(self):
        # Functionalities 6: Change Brush Blend Modes
        self.toolbar.current_brush.set_blend_mode("multiply")
        self.assertEqual(self.toolbar.current_brush.blend_mode, "multiply")

    def test_save_artwork(self):
        # Functionalities 7: Save Artwork Easily
        self.canvas.save_artwork("test_artwork.png")
        # Check if the file exists (not implemented)
        self.fail("Artwork saving verification not implemented")

    def test_export_artwork(self):
        # Functionalities 8: Export Artwork in Various File Formats
        # Exporting artwork (not implemented)
        self.fail("Artwork exporting verification not implemented")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
