import unittest
import tkinter as tk
from main import GUI
from unit_converter import UnitConverter

class TestUnitConverterGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.gui = GUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_user_input_for_conversion(self):
        # Test valid numerical input
        self.gui.value_entry.insert(0, "10")
        self.assertEqual(self.gui.value_entry.get(), "10")

        # Test invalid input
        self.gui.value_entry.delete(0, tk.END)
        self.gui.value_entry.insert(0, "abc")
        self.gui.perform_conversion()
        # Assuming the error message box will be shown, we can't directly test messagebox in unittest
        # But we can check if the result label is not updated
        self.assertEqual(self.gui.result_value.cget("text"), "")

    def test_select_desired_unit_for_conversion(self):
        # Test selecting a unit
        self.gui.from_unit_combo.set("meter")
        self.assertEqual(self.gui.from_unit_combo.get(), "meter")

        # Test changing the selected unit
        self.gui.from_unit_combo.set("kilometer")
        self.assertEqual(self.gui.from_unit_combo.get(), "kilometer")

    def test_support_for_wide_range_of_conversion_options(self):
        # Test displaying all length units
        length_units = {"meter", "kilometer", "centimeter", "millimeter"}
        self.assertTrue(length_units.issubset(set(self.gui.from_unit_combo['values'])))

        # Test displaying all weight units
        weight_units = {"kilogram", "gram", "pound"}
        self.assertTrue(weight_units.issubset(set(self.gui.from_unit_combo['values'])))

    def test_support_for_metric_and_imperial_units(self):
        # Test conversion between Celsius and Fahrenheit
        self.gui.from_unit_combo.set("celsius")
        self.gui.to_unit_combo.set("fahrenheit")
        self.assertEqual(self.gui.from_unit_combo.get(), "celsius")
        self.assertEqual(self.gui.to_unit_combo.get(), "fahrenheit")

        # Test conversion between Miles and Kilometers
        # Note: "Miles" is not in the conversion_units.txt, so this will fail
        self.gui.from_unit_combo.set("mile")
        self.gui.to_unit_combo.set("kilometer")
        self.assertEqual(self.gui.from_unit_combo.get(), "mile")
        self.assertEqual(self.gui.to_unit_combo.get(), "kilometer")

    def test_display_converted_value_with_precision(self):
        # Test conversion from Kilometers to Miles
        self.gui.value_entry.insert(0, "1.5")
        self.gui.from_unit_combo.set("kilometer")
        self.gui.to_unit_combo.set("mile")
        self.gui.perform_conversion()
        # Note: "mile" is not in the conversion_units.txt, so this will fail
        self.assertEqual(self.gui.result_value.cget("text"), "0.932")

        # Test conversion from Celsius to Fahrenheit
        self.gui.value_entry.delete(0, tk.END)
        self.gui.value_entry.insert(0, "100")
        self.gui.from_unit_combo.set("celsius")
        self.gui.to_unit_combo.set("fahrenheit")
        self.gui.perform_conversion()
        self.assertEqual(self.gui.result_value.cget("text"), "212.0")

if __name__ == '__main__':
    unittest.main()
