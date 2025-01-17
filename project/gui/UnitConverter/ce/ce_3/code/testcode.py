import unittest
from unittest.mock import MagicMock
import tkinter as tk
from GUI import GUI
from UnitConverter import UnitConverter

class TestUnitConverterGUI(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()
        self.converter.load_units('units.txt')
        self.app = GUI(self.converter)
        self.app.window.update_idletasks()

    def test_user_input_for_conversion(self):
        # Test valid input
        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "10")
        self.assertEqual(self.app.input_value.get(), "10")

        # Test invalid input
        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "abc")
        try:
            self.app.perform_conversion()
            self.fail("Expected ValueError for invalid input")
        except ValueError:
            pass

    def test_select_desired_unit_for_conversion(self):
        # Test selecting a unit
        self.app.from_unit.set("meter")
        self.assertEqual(self.app.from_unit.get(), "meter")

        # Test changing the selected unit
        self.app.from_unit.set("foot")
        self.assertEqual(self.app.from_unit.get(), "foot")

    def test_support_for_wide_range_of_conversion_options(self):
        # This functionality is not implemented in the codebase
        self.fail("Support for conversion categories like 'Length' and 'Weight' is not implemented")

    def test_support_for_metric_and_imperial_units(self):
        # This functionality is not implemented in the codebase
        self.fail("Support for 'Temperature' conversion is not implemented")

    def test_display_converted_value_with_precision(self):
        # Test conversion with precision
        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "1.5")
        self.app.from_unit.set("kilometer")
        self.app.to_unit.set("mile")
        self.app.perform_conversion()
        self.assertAlmostEqual(float(self.app.result_label.cget("text")), 0.932, places=3)

        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "100")
        self.app.from_unit.set("celsius")
        self.app.to_unit.set("fahrenheit")
        try:
            self.app.perform_conversion()
            self.fail("Expected ValueError for unsupported conversion")
        except ValueError:
            pass

if __name__ == '__main__':
    unittest.main()
