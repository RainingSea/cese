import unittest
from main import BMI_Calculator

class TestBMICalculator(unittest.TestCase):

    def test_user_input_valid(self):
        # Functionality 1: User Input for Weight and Height
        calculator = BMI_Calculator(70, 1.75)
        self.assertEqual(calculator.weight, 70)
        self.assertEqual(calculator.height, 1.75)

    def test_user_input_invalid(self):
        # Functionality 1: User Input for Weight and Height
        with self.assertRaises(ValueError):
            BMI_Calculator(-70, 0)

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        calculator = BMI_Calculator(70, 1.75)
        self.assertEqual(calculator.calculate_bmi(), 22.86)

        calculator = BMI_Calculator(50, 1.60)
        self.assertEqual(calculator.calculate_bmi(), 19.53)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        calculator = BMI_Calculator(70, 1.75)
        calculator.calculate_bmi()
        self.assertEqual(calculator.classify_bmi(), "Normal weight")

        calculator = BMI_Calculator(90, 1.75)
        calculator.calculate_bmi()
        self.assertEqual(calculator.classify_bmi(), "Overweight")

    def test_view_interpretation(self):
        # Functionality 4: View Interpretation of BMI
        calculator = BMI_Calculator(70, 1.75)
        calculator.calculate_bmi()
        calculator.classification = calculator.classify_bmi()
        self.assertEqual(calculator.get_interpretation(), "You have a healthy weight. Keep it up!")

        calculator = BMI_Calculator(50, 1.70)
        calculator.calculate_bmi()
        calculator.classification = calculator.classify_bmi()
        self.assertEqual(calculator.get_interpretation(), "You may need to gain weight for optimal health.")

    def test_provide_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        calculator = BMI_Calculator(70, 1.75)
        calculator.calculate_bmi()
        calculator.classification = calculator.classify_bmi()
        self.assertEqual(calculator.get_recommendation(), "Maintain your current lifestyle.")

        calculator = BMI_Calculator(95, 1.75)
        calculator.calculate_bmi()
        calculator.classification = calculator.classify_bmi()
        self.assertEqual(calculator.get_recommendation(), "Seek guidance from a healthcare professional.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        calculator = BMI_Calculator(70, 1.75)
        calculator.calculate_bmi()
        calculator.classification = calculator.classify_bmi()
        calculator.interpretation = calculator.get_interpretation()
        calculator.recommendation = calculator.get_recommendation()
        calculator.store_data()

        with open('bmi_data.txt', 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip()
            self.assertEqual(last_line, "70,1.75,22.86,Normal weight,You have a healthy weight. Keep it up!,Maintain your current lifestyle.")

if __name__ == '__main__':
    unittest.main()
