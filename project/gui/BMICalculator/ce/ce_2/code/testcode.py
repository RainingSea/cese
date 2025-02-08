import unittest
from bmi_calculator import BMICalculator
import os

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        # This method will be run before each test
        self.calculator = None
        self.test_file = 'bmi_data.txt'
        # Ensure the test file is empty before each test
        open(self.test_file, 'w').close()

    def test_user_input(self):
        # Functionality 1: User Input for Weight and Height
        # Valid input
        try:
            self.calculator = BMICalculator(70, 1.75)
        except ValueError:
            self.fail("BMICalculator raised ValueError unexpectedly for valid input!")

        # Invalid input
        with self.assertRaises(ValueError):
            self.calculator = BMICalculator(-70, 0)

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        self.calculator = BMICalculator(70, 1.75)
        self.assertAlmostEqual(self.calculator.calculate_bmi(), 22.86, places=2)

        self.calculator = BMICalculator(50, 1.60)
        self.assertAlmostEqual(self.calculator.calculate_bmi(), 19.53, places=2)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        self.calculator = BMICalculator(70, 1.75)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.classify_bmi(bmi), "Normal weight")

        self.calculator = BMICalculator(90, 1.75)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.classify_bmi(bmi), "Overweight")

    def test_interpret_bmi(self):
        # Functionality 4: View Interpretation of BMI
        self.calculator = BMICalculator(70, 1.75)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.interpret_bmi(bmi), "You have a normal weight. Keep up the good work!")

        self.calculator = BMICalculator(50, 1.70)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.interpret_bmi(bmi), "You are underweight. Consider consulting a healthcare provider.")

    def test_recommendation(self):
        # Functionality 5: Provide BMI Recommendations
        self.calculator = BMICalculator(70, 1.75)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.recommendation(bmi), "Maintain your current lifestyle.")

        self.calculator = BMICalculator(95, 1.75)
        bmi = self.calculator.calculate_bmi()
        self.assertEqual(self.calculator.recommendation(bmi), "Consult a healthcare provider for a personalized plan.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.calculator = BMICalculator(70, 1.75)
        bmi = self.calculator.calculate_bmi()
        category = self.calculator.classify_bmi(bmi)
        interpretation = self.calculator.interpret_bmi(bmi)
        recommendation = self.calculator.recommendation(bmi)
        self.calculator.save_data(70, 1.75, bmi, category, interpretation, recommendation)

        # Check if data is saved correctly
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)
            self.assertIn("70,1.75,22.86,Normal weight,You have a normal weight. Keep up the good work!,Maintain your current lifestyle.", lines[0])

if __name__ == '__main__':
    unittest.main()
