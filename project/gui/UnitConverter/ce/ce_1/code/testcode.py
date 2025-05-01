import unittest
import os
import subprocess

class TestUnitConverter(unittest.TestCase):

    def setUp(self):
        # Ensure the conversion_data.txt file exists for testing
        self.conversion_data_path = 'conversion_data.txt'
        if not os.path.exists(self.conversion_data_path):
            with open(self.conversion_data_path, 'w') as f:
                f.write("meter|kilometer|0.001\n")
                f.write("kilometer|meter|1000\n")
                f.write("meter|centimeter|100\n")
                f.write("centimeter|meter|0.01\n")
                f.write("liter|milliliter|1000\n")
                f.write("milliliter|liter|0.001\n")
                f.write("kilogram|gram|1000\n")
                f.write("gram|kilogram|0.001\n")

    def test_user_input_conversion(self):
        # Functionality 1: User Input for Conversion
        # Test valid input
        result = subprocess.run(['python', 'main.py'], input='10\n', text=True, capture_output=True)
        self.assertIn("Result:", result.stdout)

        # Test invalid input
        result = subprocess.run(['python', 'main.py'], input='abc\n', text=True, capture_output=True)
        self.assertIn("invalid input", result.stdout)

    def test_select_desired_unit(self):
        # Functionality 2: Select Desired Unit for Conversion
        # Test selecting a unit
        result = subprocess.run(['python', 'main.py'], input='10\nmeter\nkilometer\n', text=True, capture_output=True)
        self.assertIn("kilometer", result.stdout)

    def test_conversion_options(self):
        # Functionality 3: Support for a Wide Range of Conversion Options
        # Test length units
        result = subprocess.run(['python', 'main.py'], input='10\nmeter\nkilometer\n', text=True, capture_output=True)
        self.assertIn("kilometer", result.stdout)

        # Test weight units (not implemented in the current code)
        self.fail("Weight conversion options not implemented.")

    def test_metric_imperial_conversion(self):
        # Functionality 4: Support for Both Metric and Imperial Units
        # Test Celsius to Fahrenheit conversion (not implemented in the current code)
        self.fail("Celsius to Fahrenheit conversion not implemented.")

        # Test Miles to Kilometers conversion (not implemented in the current code)
        self.fail("Miles to Kilometers conversion not implemented.")

    def test_display_converted_value(self):
        # Functionality 5: Display Converted Value with Precision
        # Test conversion from Kilometers to Miles
        result = subprocess.run(['python', 'main.py'], input='1.5\nkilometer\nmile\n', text=True, capture_output=True)
        self.assertIn("0.932", result.stdout)

        # Test conversion from Celsius to Fahrenheit
        result = subprocess.run(['python', 'main.py'], input='100\nCelsius\nFahrenheit\n', text=True, capture_output=True)
        self.assertIn("212.0", result.stdout)

if __name__ == '__main__':
    unittest.main()
