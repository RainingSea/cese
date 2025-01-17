import unittest
from UnitConverter import UnitConverter
from GUI import GUI
import tkinter as tk

class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()
        self.converter.load_conversion_factors('conversion_factors.txt')
        self.app = GUI(self.converter)

    def test_user_input_for_conversion(self):
        # Test valid numerical input
        self.app.value_entry.insert(0, "10")
        self.assertEqual(self.app.value_entry.get(), "10")
        self.app.value_entry.delete(0, tk.END)

        # Test invalid input
        self.app.value_entry.insert(0, "abc")
        self.app.perform_conversion()
        self.assertIn("Error", self.app.result_label.cget("text"))
        self.app.value_entry.delete(0, tk.END)

    def test_select_desired_unit_for_conversion(self):
        # Test selecting a unit
        self.app.from_unit.set("meter")
        self.assertEqual(self.app.from_unit.get(), "meter")

        # Test changing the selected unit
        self.app.from_unit.set("kilometer")
        self.assertEqual(self.app.from_unit.get(), "kilometer")

    def test_support_for_wide_range_of_conversion_options(self):
        # Test length units
        length_units = ["meter", "kilometer"]
        self.assertTrue(all(unit in self.app.from_unit['values'] for unit in length_units))

        # Test weight units
        weight_units = ["gram", "kilogram"]
        self.assertTrue(all(unit in self.app.from_unit['values'] for unit in weight_units))

    def test_support_for_metric_and_imperial_units(self):
        # Test temperature conversion
        self.app.from_unit.set("celsius")
        self.app.to_unit.set("fahrenheit")
        self.assertEqual(self.app.from_unit.get(), "celsius")
        self.assertEqual(self.app.to_unit.get(), "fahrenheit")

        # Test length conversion (Note: Miles is not in the conversion_factors.txt, so this will fail)
        self.app.from_unit.set("mile")
        self.app.to_unit.set("kilometer")
        self.assertEqual(self.app.from_unit.get(), "mile")
        self.assertEqual(self.app.to_unit.get(), "kilometer")

    def test_display_converted_value_with_precision(self):
        # Test conversion with precision
        self.app.value_entry.insert(0, "1.5")
        self.app.from_unit.set("kilometer")
        self.app.to_unit.set("meter")
        self.app.perform_conversion()
        self.assertAlmostEqual(float(self.app.result_label.cget("text").split(": ")[1]), 1500.0, places=2)
        self.app.value_entry.delete(0, tk.END)

        self.app.value_entry.insert(0, "100")
        self.app.from_unit.set("celsius")
        self.app.to_unit.set("fahrenheit")
        self.app.perform_conversion()
        self.assertAlmostEqual(float(self.app.result_label.cget("text").split(": ")[1]), 212.0, places=1)
        self.app.value_entry.delete(0, tk.END)

if __name__ == '__main__':
    unittest.main()
