import unittest
from conversion import UnitConverter
import tkinter as tk
from gui import GUI

class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()
        self.converter.load_conversion_factors('conversion_factors.txt')
        self.app = GUI(self.converter)

    def test_user_input_for_conversion(self):
        # Test valid input
        self.app.input_value.insert(0, "10")
        self.assertEqual(self.app.input_value.get(), "10")
        
        # Test invalid input
        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "abc")
        try:
            value = float(self.app.input_value.get())
            self.fail("Expected ValueError for invalid input")
        except ValueError:
            pass

    def test_select_desired_unit_for_conversion(self):
        # Test selecting a unit
        self.app.from_unit.set("length,meter")
        self.assertEqual(self.app.from_unit.get(), "length,meter")
        
        # Test changing the selected unit
        self.app.from_unit.set("length,kilometer")
        self.assertEqual(self.app.from_unit.get(), "length,kilometer")

    def test_support_for_wide_range_of_conversion_options(self):
        # Test length units
        length_units = [key for key in self.converter.conversion_factors.keys() if key[0] == 'length']
        self.assertIn(('length', 'meter'), length_units)
        self.assertIn(('length', 'kilometer'), length_units)

        # Test weight units
        weight_units = [key for key in self.converter.conversion_factors.keys() if key[0] == 'weight']
        self.assertIn(('weight', 'gram'), weight_units)
        self.assertIn(('weight', 'kilogram'), weight_units)

    def test_support_for_metric_and_imperial_units(self):
        # This functionality is not implemented in the codebase
        self.fail("Support for temperature and imperial units not implemented")

    def test_display_converted_value_with_precision(self):
        # Test conversion with precision
        self.app.input_value.insert(0, "1.5")
        self.app.from_unit.set("length,kilometer")
        self.app.to_unit.set("length,meter")
        self.app.perform_conversion()
        self.assertEqual(self.app.result_label.cget("text"), "Result: 1500.0")

        self.app.input_value.delete(0, tk.END)
        self.app.input_value.insert(0, "100")
        self.app.from_unit.set("weight,gram")
        self.app.to_unit.set("weight,kilogram")
        self.app.perform_conversion()
        self.assertEqual(self.app.result_label.cget("text"), "Result: 0.1")

if __name__ == '__main__':
    unittest.main()
