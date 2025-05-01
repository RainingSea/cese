import unittest
import os
from main import UnitConverter, GUI

class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        self.converter = UnitConverter()
        self.converter.load_conversion_rates('conversion_rates.txt')

    def test_user_input_conversion(self):
        # Functionality 1: User Input for Conversion
        # Valid input
        try:
            value = self.converter.convert(10, 'meters', 'kilometers')
            self.assertEqual(value, 0.01)  # 10 meters to kilometers
        except Exception as e:
            self.fail(f"Valid input raised an exception: {str(e)}")

        # Invalid input
        with self.assertRaises(ValueError):
            self.converter.convert(10, 'meters', 'invalid_unit')

    def test_select_desired_unit(self):
        # Functionality 2: Select Desired Unit for Conversion
        # Check if units are loaded correctly
        self.assertIn(('meters', 'kilometers'), self.converter.conversion_rates)
        self.assertIn(('grams', 'kilograms'), self.converter.conversion_rates)

    def test_conversion_options(self):
        # Functionality 3: Support for a Wide Range of Conversion Options
        # Check if conversion options are available
        self.assertIn(('celsius', 'fahrenheit'), self.converter.conversion_rates)
        self.assertIn(('fahrenheit', 'celsius'), self.converter.conversion_rates)

    def test_metric_imperial_conversion(self):
        # Functionality 4: Support for Both Metric and Imperial Units
        # Metric to Imperial
        result = self.converter.convert(100, 'celsius', 'fahrenheit')
        self.assertAlmostEqual(result, 212.0, places=1)  # 100 Celsius to Fahrenheit

        # Imperial to Metric
        result = self.converter.convert(1, 'miles', 'kilometers')
        self.assertAlmostEqual(result, 1.60934, places=5)  # 1 Mile to Kilometers

    def test_display_converted_value_precision(self):
        # Functionality 5: Display Converted Value with Precision
        result = self.converter.convert(1.5, 'kilometers', 'miles')
        self.assertAlmostEqual(result, 0.932, places=3)  # 1.5 Kilometers to Miles

        result = self.converter.convert(100, 'celsius', 'fahrenheit')
        self.assertAlmostEqual(result, 212.0, places=1)  # 100 Celsius to Fahrenheit

if __name__ == '__main__':
    unittest.main()
