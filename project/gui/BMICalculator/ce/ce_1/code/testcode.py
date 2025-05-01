import unittest
import os
from main import BMI_Calculator

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        self.bmi_calculator = BMI_Calculator()

    def test_user_input_valid(self):
        # Functionality 1: User Input for Weight and Height
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        self.assertEqual(self.bmi_calculator.weight, 70)
        self.assertEqual(self.bmi_calculator.height, 1.75)

    def test_user_input_invalid(self):
        # Functionality 1: Invalid Input Handling
        with self.assertRaises(ValueError):
            self.bmi_calculator.weight = -70
            self.bmi_calculator.height = 0
            self.bmi_calculator.calculate_bmi()

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        self.assertAlmostEqual(bmi, 22.86, places=2)

        self.bmi_calculator.weight = 50
        self.bmi_calculator.height = 1.60
        bmi = self.bmi_calculator.calculate_bmi()
        self.assertAlmostEqual(bmi, 19.53, places=2)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        classification = self.bmi_calculator.classify_bmi(bmi)
        self.assertEqual(classification, "Normal weight")

        self.bmi_calculator.weight = 90
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        classification = self.bmi_calculator.classify_bmi(bmi)
        self.assertEqual(classification, "Overweight")

    def test_interpret_bmi(self):
        # Functionality 4: View Interpretation of BMI
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        interpretation = self.bmi_calculator.interpret_bmi(bmi)
        self.assertEqual(interpretation, "You have a normal weight. Keep up the good work!")

        self.bmi_calculator.weight = 50
        self.bmi_calculator.height = 1.70
        bmi = self.bmi_calculator.calculate_bmi()
        interpretation = self.bmi_calculator.interpret_bmi(bmi)
        self.assertEqual(interpretation, "You are underweight. It's advisable to consult a healthcare provider.")

    def test_provide_bmi_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        classification = self.bmi_calculator.classify_bmi(bmi)
        recommendation = self.bmi_calculator.recommendation(classification)
        self.assertEqual(recommendation, "Maintain your current lifestyle.")

        self.bmi_calculator.weight = 95
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        classification = self.bmi_calculator.classify_bmi(bmi)
        recommendation = self.bmi_calculator.recommendation(classification)
        self.assertEqual(recommendation, "Consult a healthcare provider for a personalized plan.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.bmi_calculator.weight = 70
        self.bmi_calculator.height = 1.75
        bmi = self.bmi_calculator.calculate_bmi()
        classification = self.bmi_calculator.classify_bmi(bmi)
        interpretation = self.bmi_calculator.interpret_bmi(bmi)
        recommendation = self.bmi_calculator.recommendation(classification)

        # Save result
        self.bmi_calculator.save_result(self.bmi_calculator.weight, self.bmi_calculator.height, bmi, classification, interpretation, recommendation)

        # Check if the result is saved correctly
        with open('bmi_results.txt', 'r') as file:
            lines = file.readlines()
            last_entry = lines[-1].strip().split(',')
            self.assertEqual(float(last_entry[0]), 70)
            self.assertEqual(float(last_entry[1]), 1.75)
            self.assertAlmostEqual(float(last_entry[2]), bmi, places=2)
            self.assertEqual(last_entry[3], classification)
            self.assertEqual(last_entry[4], interpretation)
            self.assertEqual(last_entry[5], recommendation)

if __name__ == '__main__':
    unittest.main()
