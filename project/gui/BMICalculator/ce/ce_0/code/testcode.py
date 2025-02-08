import unittest
from bmi_calculator import BMI_Calculator
import os

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        # This method will be run before each test
        self.valid_weight = 70
        self.valid_height = 1.75
        self.invalid_weight = -70
        self.invalid_height = 0
        self.bmi_calculator = BMI_Calculator(self.valid_weight, self.valid_height)

    def test_user_input_valid(self):
        # Functionality 1: User Input for Weight and Height
        try:
            BMI_Calculator(self.valid_weight, self.valid_height)
        except ValueError:
            self.fail("BMI_Calculator raised ValueError unexpectedly!")

    def test_user_input_invalid(self):
        with self.assertRaises(ValueError):
            BMI_Calculator(self.invalid_weight, self.invalid_height)

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        bmi_calculator = BMI_Calculator(70, 1.75)
        self.assertEqual(bmi_calculator.bmi, 22.86)

        bmi_calculator = BMI_Calculator(50, 1.60)
        self.assertEqual(bmi_calculator.bmi, 19.53)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        bmi_calculator = BMI_Calculator(70, 1.75)
        self.assertEqual(bmi_calculator.classify_bmi(), "Normal weight")

        bmi_calculator = BMI_Calculator(90, 1.75)
        self.assertEqual(bmi_calculator.classify_bmi(), "Overweight")

    def test_interpret_bmi(self):
        # Functionality 4: View Interpretation of BMI
        bmi_calculator = BMI_Calculator(70, 1.75)
        self.assertIn("healthy weight range", bmi_calculator.interpret_bmi())

        bmi_calculator = BMI_Calculator(50, 1.70)
        self.assertIn("under the recommended weight range", bmi_calculator.interpret_bmi())

    def test_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        bmi_calculator = BMI_Calculator(70, 1.75)
        self.assertIn("balanced diet and regular exercise", bmi_calculator.recommendations())

        bmi_calculator = BMI_Calculator(95, 1.75)
        self.assertIn("Seek guidance from a healthcare provider", bmi_calculator.recommendations())

    def test_data_storage(self):
        # Functionality 6: Data Storage
        bmi_calculator = BMI_Calculator(70, 1.75)
        bmi_calculator.save_data()

        with open('bmi_data.txt', 'r') as file:
            data = file.readlines()
            self.assertIn("70|1.75|22.86|Normal weight", data[-1])

if __name__ == '__main__':
    unittest.main()
