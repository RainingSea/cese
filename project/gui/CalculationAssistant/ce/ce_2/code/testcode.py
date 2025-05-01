import unittest
import os
import math
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.app = CalculationAssistant()
        self.app.input1.insert(0, '0')
        self.app.input2.insert(0, '0')
        self.result_file = 'calculations.txt'
        # Clear the result file before each test
        if os.path.exists(self.result_file):
            os.remove(self.result_file)

    def test_basic_arithmetic_operations(self):
        # Functionalities 1: Perform Basic Arithmetic Operations
        # Addition
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '5')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '3')
        self.app.add()
        self.assertEqual(self.app.result_display.cget("text"), "8.0")

        # Subtraction
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '7')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '-2')
        self.app.subtract()
        self.assertEqual(self.app.result_display.cget("text"), "9.0")

        # Multiplication
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '4')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '6')
        self.app.multiply()
        self.assertEqual(self.app.result_display.cget("text"), "24.0")

        # Division
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '8')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '2')
        self.app.divide()
        self.assertEqual(self.app.result_display.cget("text"), "4.0")

        # Division by zero
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '10')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '0')
        with self.assertRaises(Exception):
            self.app.divide()
            self.assertIn("Cannot divide by zero.", self.app.result_display.cget("text"))

    def test_square_root(self):
        # Functionalities 2: Calculate Square Roots
        # Positive integer
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '16')
        self.app.square_root()
        self.assertEqual(self.app.result_display.cget("text"), "4.0")

        # Zero
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.square_root()
        self.assertEqual(self.app.result_display.cget("text"), "0.0")

        # Negative number
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '-9')
        with self.assertRaises(ValueError):
            self.app.square_root()
            self.assertIn("Invalid input for square root", self.app.result_display.cget("text"))

    def test_exponentiation(self):
        # Functionalities 3: Perform Exponentiation Calculations
        # Positive base and exponent
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '2')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '3')
        self.app.exponentiate()
        self.assertEqual(self.app.result_display.cget("text"), "8.0")

        # Base of zero and positive exponent
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '5')
        self.app.exponentiate()
        self.assertEqual(self.app.result_display.cget("text"), "0.0")

        # Positive base and zero exponent
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '7')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '0')
        self.app.exponentiate()
        self.assertEqual(self.app.result_display.cget("text"), "1.0")

        # Negative base and even exponent
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '-3')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '2')
        self.app.exponentiate()
        self.assertEqual(self.app.result_display.cget("text"), "9.0")

    def test_percentage(self):
        # Functionalities 4: Calculate Percentages
        # Positive number and percentage
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '200')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '10')
        self.app.percentage()
        self.assertEqual(self.app.result_display.cget("text"), "20.0")

        # Zero and any percentage
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '25')
        self.app.percentage()
        self.assertEqual(self.app.result_display.cget("text"), "0.0")

        # Negative number and percentage
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '-50')
        self.app.input2.delete(0, 'end')
        self.app.input2.insert(0, '10')
        self.app.percentage()
        self.assertEqual(self.app.result_display.cget("text"), "-5.0")

if __name__ == '__main__':
    unittest.main()
