import unittest
from BMI_Calculator import BMI_Calculator

class TestBMICalculator(unittest.TestCase):

    def test_user_input(self):
        # Functionality 1: User Input for Weight and Height
        # Valid input
        calculator = BMI_Calculator(70, 1.75)
        self.assertEqual(calculator.weight, 70)
        self.assertEqual(calculator.height, 1.75)

        # Invalid input
        with self.assertRaises(ValueError):
            BMI_Calculator(-70, 0)

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        calculator = BMI_Calculator(70, 1.75)
        self.assertAlmostEqual(calculator.calculate_bmi(), 22.86, places=2)

        calculator = BMI_Calculator(50, 1.60)
        self.assertAlmostEqual(calculator.calculate_bmi(), 19.53, places=2)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        calculator = BMI_Calculator(70, 1.75)
        bmi = calculator.calculate_bmi()
        self.assertEqual(calculator.classify_bmi(bmi), "Normal weight")

        calculator = BMI_Calculator(90, 1.75)
        bmi = calculator.calculate_bmi()
        self.assertEqual(calculator.classify_bmi(bmi), "Overweight")

    def test_view_interpretation_of_bmi(self):
        # Functionality 4: View Interpretation of BMI
        calculator = BMI_Calculator(70, 1.75)
        bmi = calculator.calculate_bmi()
        self.assertEqual(calculator.interpret_bmi(bmi), "You have a normal weight. Keep up the good work!")

        calculator = BMI_Calculator(50, 1.70)
        bmi = calculator.calculate_bmi()
        self.assertEqual(calculator.interpret_bmi(bmi), "You are underweight. Consider consulting a healthcare provider.")

    def test_provide_bmi_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        calculator = BMI_Calculator(70, 1.75)
        bmi = calculator.calculate_bmi()
        category = calculator.classify_bmi(bmi)
        self.assertEqual(calculator.recommendations(category), "Maintain a balanced diet and regular exercise.")

        calculator = BMI_Calculator(95, 1.75)
        bmi = calculator.calculate_bmi()
        category = calculator.classify_bmi(bmi)
        self.assertEqual(calculator.recommendations(category), "Seek guidance from a healthcare provider for a weight management plan.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        calculator = BMI_Calculator(70, 1.75)
        bmi = calculator.calculate_bmi()
        category = calculator.classify_bmi(bmi)
        interpretation = calculator.interpret_bmi(bmi)
        recommendation = calculator.recommendations(category)
        calculator.save_data(70, 1.75, bmi, category, recommendation)

        with open('bmi_data.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn("70|1.75|22.86|Normal weight|Maintain a balanced diet and regular exercise.\n", lines)

if __name__ == '__main__':
    unittest.main()
