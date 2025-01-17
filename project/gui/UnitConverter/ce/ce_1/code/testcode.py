import unittest
import tkinter as tk
from gui import GUI

class TestUnitConverterGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = GUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_user_input_for_conversion(self):
        # Test valid numerical input
        self.app.value_entry.insert(0, "10")
        self.assertEqual(self.app.value_entry.get(), "10")

        # Test invalid input
        self.app.value_entry.delete(0, tk.END)
        self.app.value_entry.insert(0, "abc")
        self.app.perform_conversion()
        self.assertIn("Error", self.app.result_label.cget("text"))

    def test_select_desired_unit_for_conversion(self):
        # Test selecting a unit from the dropdown
        self.app.from_unit_combo.set("meter")
        self.assertEqual(self.app.from_unit_combo.get(), "meter")

        # Test changing the selected unit
        self.app.from_unit_combo.set("foot")
        self.assertEqual(self.app.from_unit_combo.get(), "foot")

    def test_support_for_wide_range_of_conversion_options(self):
        # Test displaying all available length units
        length_units = ["meter", "kilometer", "centimeter", "millimeter", "inch", "foot", "yard"]
        for unit in length_units:
            self.assertIn(unit, self.app.from_unit_combo['values'])

        # Test displaying all available weight units
        weight_units = ["kilogram", "gram", "pound", "ounce"]
        for unit in weight_units:
            self.assertIn(unit, self.app.from_unit_combo['values'])

    def test_support_for_metric_and_imperial_units(self):
        # This functionality is not implemented in the codebase
        self.fail("Conversion between metric and imperial units (e.g., Celsius to Fahrenheit) is not implemented.")

    def test_display_converted_value_with_precision(self):
        # Test conversion with precision
        self.app.value_entry.insert(0, "1.5")
        self.app.from_unit_combo.set("kilometer")
        self.app.to_unit_combo.set("meter")
        self.app.perform_conversion()
        self.assertIn("Result", self.app.result_label.cget("text"))

        # Test conversion with precision for non-implemented units
        self.app.value_entry.delete(0, tk.END)
        self.app.value_entry.insert(0, "100")
        self.app.from_unit_combo.set("celsius")
        self.app.to_unit_combo.set("fahrenheit")
        self.app.perform_conversion()
        self.assertIn("Error", self.app.result_label.cget("text"))

if __name__ == '__main__':
    unittest.main()
