import unittest
import os
from tkinter import Tk
from main import Main

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = Main(self.root)

    def tearDown(self):
        self.root.destroy()
        # Clean up the user_data.txt file after tests
        if os.path.exists("user_data.txt"):
            os.remove("user_data.txt")

    def test_user_input_valid(self):
        # Functionality 1: User Input for Weight and Height
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.assertEqual(self.app.weight_entry.get(), "70")
        self.assertEqual(self.app.height_entry.get(), "1.75")

    def test_user_input_invalid(self):
        # Functionality 1: Invalid Input
        self.app.weight_entry.insert(0, "-70")
        self.app.height_entry.insert(0, "0")
        with self.assertRaises(ValueError):
            self.app.run()  # This should trigger the error message

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertEqual(self.app.result_label.cget("text"), "BMI: 22.86")

        self.app.weight_entry.delete(0, 'end')
        self.app.height_entry.delete(0, 'end')
        self.app.weight_entry.insert(0, "50")
        self.app.height_entry.insert(0, "1.60")
        self.app.run()
        self.assertEqual(self.app.result_label.cget("text"), "BMI: 19.53")

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertEqual(self.app.classification_label.cget("text"), "Classification: Normal weight")

        self.app.weight_entry.delete(0, 'end')
        self.app.height_entry.delete(0, 'end')
        self.app.weight_entry.insert(0, "90")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertEqual(self.app.classification_label.cget("text"), "Classification: Overweight")

    def test_interpretation_of_bmi(self):
        # Functionality 4: View Interpretation of BMI
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertEqual(self.app.interpretation_label.cget("text"), "Your BMI is 22.86.")

        self.app.weight_entry.delete(0, 'end')
        self.app.height_entry.delete(0, 'end')
        self.app.weight_entry.insert(0, "50")
        self.app.height_entry.insert(0, "1.70")
        self.app.run()
        self.assertEqual(self.app.interpretation_label.cget("text"), "Your BMI is 17.30.")

    def test_provide_bmi_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertIn("Maintain your current lifestyle", self.app.recommendations_label.cget("text"))

        self.app.weight_entry.delete(0, 'end')
        self.app.height_entry.delete(0, 'end')
        self.app.weight_entry.insert(0, "95")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()
        self.assertIn("Consult a healthcare provider", self.app.recommendations_label.cget("text"))

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "1.75")
        self.app.run()

        with open("user_data.txt", "r") as file:
            lines = file.readlines()
            self.assertIn("70|1.75|22.86|Normal weight\n", lines)

if __name__ == '__main__':
    unittest.main()
