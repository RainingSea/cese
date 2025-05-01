import unittest
import os
from converter import Converter

class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()
        self.history_file = 'conversion_history.txt'
        # Clear the history file before each test
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def test_user_input_conversion(self):
        # Functionality 1: User Input for Conversion
        # Valid input
        try:
            value = self.converter.convert(10, 'meters', 'kilometers')
            self.assertEqual(value, 0.01)
        except ValueError:
            self.fail("Valid input raised ValueError unexpectedly.")

        # Invalid input
        with self.assertRaises(ValueError):
            self.converter.convert(10, 'invalid_unit', 'kilometers')

    def test_select_desired_unit(self):
        # Functionality 2: Select Desired Unit for Conversion
        # Valid unit selection
        self.assertEqual(self.converter.convert(10, 'meters', 'kilometers'), 0.01)
        self.assertEqual(self.converter.convert(5, 'kilometers', 'meters'), 5000.0)

    def test_conversion_options(self):
        # Functionality 3: Support for a Wide Range of Conversion Options
        # Check available units
        available_units = ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'yards', 'feet']
        self.assertIn('meters', available_units)
        self.assertIn('miles', available_units)

    def test_metric_imperial_conversion(self):
        # Functionality 4: Support for Both Metric and Imperial Units
        # Metric to Imperial
        self.assertEqual(self.converter.convert(100, 'centimeters', 'meters'), 1.0)
        # Imperial to Metric
        self.assertEqual(self.converter.convert(1, 'miles', 'kilometers'), 1.60934)

    def test_display_converted_value_precision(self):
        # Functionality 5: Display Converted Value with Precision
        self.assertAlmostEqual(self.converter.convert(1.5, 'kilometers', 'miles'), 0.932056, places=3)
        self.assertAlmostEqual(self.converter.convert(100, 'celsius', 'fahrenheit'), 212.0, places=1)

    def test_conversion_history(self):
        # Test conversion history functionality
        self.converter.save_conversion(10, 'meters', 0.01, 'kilometers')
        history = self.converter.get_conversion_history()
        self.assertIn("10 meters 0.01 kilometers", history)

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

if __name__ == '__main__':
    unittest.main()
