import unittest
import tkinter as tk
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.app = CalculationAssistant()
        self.app.root.update()

    def tearDown(self):
        self.app.root.destroy()

    def test_basic_arithmetic_operations(self):
        # Test addition
        self.app.input1.set("5")
        self.app.input2.set("3")
        self.app.perform_addition()
        self.assertIn("Result: 8.0", self.app.result_display.get("1.0", tk.END))

        # Test subtraction
        self.app.input1.set("7")
        self.app.input2.set("-2")
        self.app.perform_subtraction()
        self.assertIn("Result: 9.0", self.app.result_display.get("1.0", tk.END))

        # Test multiplication
        self.app.input1.set("4")
        self.app.input2.set("6")
        self.app.perform_multiplication()
        self.assertIn("Result: 24.0", self.app.result_display.get("1.0", tk.END))

        # Test division
        self.app.input1.set("8")
        self.app.input2.set("2")
        self.app.perform_division()
        self.assertIn("Result: 4.0", self.app.result_display.get("1.0", tk.END))

        # Test division by zero
        self.app.input1.set("10")
        self.app.input2.set("0")
        with self.assertRaises(tk.TclError):
            self.app.perform_division()

    def test_calculate_square_roots(self):
        # Test square root of positive number
        self.app.input1.set("16")
        self.app.calculate_square_root()
        self.assertIn("Result: 4.0", self.app.result_display.get("1.0", tk.END))

        # Test square root of zero
        self.app.input1.set("0")
        self.app.calculate_square_root()
        self.assertIn("Result: 0.0", self.app.result_display.get("1.0", tk.END))

        # Test square root of negative number
        self.app.input1.set("-9")
        with self.assertRaises(ValueError):
            self.app.calculate_square_root()

    def test_exponentiation_calculations(self):
        # Test exponentiation with positive base and exponent
        self.app.input1.set("2")
        self.app.input2.set("3")
        self.app.perform_exponentiation()
        self.assertIn("Result: 8.0", self.app.result_display.get("1.0", tk.END))

        # Test exponentiation with base zero and positive exponent
        self.app.input1.set("0")
        self.app.input2.set("5")
        self.app.perform_exponentiation()
        self.assertIn("Result: 0.0", self.app.result_display.get("1.0", tk.END))

        # Test exponentiation with positive base and zero exponent
        self.app.input1.set("7")
        self.app.input2.set("0")
        self.app.perform_exponentiation()
        self.assertIn("Result: 1.0", self.app.result_display.get("1.0", tk.END))

        # Test exponentiation with negative base and even exponent
        self.app.input1.set("-3")
        self.app.input2.set("2")
        self.app.perform_exponentiation()
        self.assertIn("Result: 9.0", self.app.result_display.get("1.0", tk.END))

    def test_calculate_percentages(self):
        # Test percentage calculation with positive number
        self.app.input1.set("200")
        self.app.input2.set("10")
        self.app.calculate_percentage()
        self.assertIn("Result: 20.0", self.app.result_display.get("1.0", tk.END))

        # Test percentage calculation with zero
        self.app.input1.set("0")
        self.app.input2.set("25")
        self.app.calculate_percentage()
        self.assertIn("Result: 0.0", self.app.result_display.get("1.0", tk.END))

        # Test percentage calculation with negative number
        self.app.input1.set("-50")
        self.app.input2.set("10")
        self.app.calculate_percentage()
        self.assertIn("Result: -5.0", self.app.result_display.get("1.0", tk.END))

if __name__ == '__main__':
    unittest.main()
