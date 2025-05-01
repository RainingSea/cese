import unittest
import os
from main import BMI_Calculator

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        self.bmi_calculator = BMI_Calculator()

    def test_user_input(self):
        # Functionality 1: User Input for Weight and Height
        # Valid input
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.weight, 70)
        self.assertEqual(self.bmi_calculator.height, 1.75)

        # Invalid input (simulated)
        with self.assertRaises(ValueError):
            self.bmi_calculator.weight = -70
            self.bmi_calculator.height = 0

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertAlmostEqual(self.bmi_calculator.calculate_bmi(), 22.86, places=2)

        self.bmi_calculator.weight = 50
        self.bmi_calculator.height = 1.60
        self.assertAlmostEqual(self.bmi_calculator.calculate_bmi(), 19.53, places=2)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.classify_bmi(), "Normal weight")

        self.bmi_calculator.weight = 90
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.classify_bmi(), "Overweight")

    def test_interpret_bmi(self):
        # Functionality 4: View Interpretation of BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.interpret_bmi(), "You have a normal weight. Keep up the good work!")

        self.bmi_calculator.weight = 50
        self.bmi_calculator.height = 1.70
        self.assertEqual(self.bmi_calculator.interpret_bmi(), "You are underweight. It's advisable to consult a healthcare provider.")

    def test_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.recommendations(), "Maintain your current lifestyle.")

        self.bmi_calculator.weight = 95
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.recommendations(), "Engage in regular physical activity and monitor your diet.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.bmi_calculator.save_data(self.bmi_calculator.weight, self.bmi_calculator.height)

        # Check if the data is saved correctly
        with open('bmi_data.txt', 'r') as file:
            lines = file.readlines()
            self.assertTrue(any("70|1.75|" in line for line in lines))

        # Clean up the file after test
        os.remove('bmi_data.txt')

if __name__ == '__main__':
    unittest.main()
