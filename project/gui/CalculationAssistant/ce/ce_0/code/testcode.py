import unittest
import pyautogui
import time
import subprocess

class TestCalculationAssistant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the CalculationAssistant application
        cls.process = subprocess.Popen(['python', 'D:/Project/CE/CE/project/gui/CalculationAssistant/ce/ce_0/code/main.py'])
        time.sleep(2)  # Wait for the GUI to initialize

    @classmethod
    def tearDownClass(cls):
        # Terminate the CalculationAssistant application
        cls.process.terminate()

    def test_basic_arithmetic_operations(self):
        # Test addition
        pyautogui.write('5', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('3', interval=0.1)
        pyautogui.press('tab', presses=2)
        pyautogui.press('enter')  # Assuming the "Add" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for addition', title='Result Check', default='')
        self.assertEqual(result, 'Result: 8.0')

        # Test subtraction
        pyautogui.write('7', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('-2', interval=0.1)
        pyautogui.press('tab', presses=3)
        pyautogui.press('enter')  # Assuming the "Subtract" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for subtraction', title='Result Check', default='')
        self.assertEqual(result, 'Result: 9.0')

        # Test multiplication
        pyautogui.write('4', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('6', interval=0.1)
        pyautogui.press('tab', presses=4)
        pyautogui.press('enter')  # Assuming the "Multiply" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for multiplication', title='Result Check', default='')
        self.assertEqual(result, 'Result: 24.0')

        # Test division
        pyautogui.write('8', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab', presses=5)
        pyautogui.press('enter')  # Assuming the "Divide" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for division', title='Result Check', default='')
        self.assertEqual(result, 'Result: 4.0')

        # Test division by zero
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab', presses=5)
        pyautogui.press('enter')  # Assuming the "Divide" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for division by zero', title='Result Check', default='')
        self.assertEqual(result, 'Error: Division by zero')

    def test_square_root(self):
        # Test square root of a positive number
        pyautogui.write('16', interval=0.1)
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')  # Assuming the "Square Root" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for square root', title='Result Check', default='')
        self.assertEqual(result, 'Result: 4.0')

        # Test square root of zero
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')  # Assuming the "Square Root" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for square root of zero', title='Result Check', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test square root of a negative number
        pyautogui.write('-9', interval=0.1)
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')  # Assuming the "Square Root" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for square root of negative number', title='Result Check', default='')
        self.assertEqual(result, 'Error: Invalid input for square root')

    def test_exponentiation(self):
        # Test exponentiation with positive base and exponent
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('3', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')  # Assuming the "Exponentiate" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for exponentiation', title='Result Check', default='')
        self.assertEqual(result, 'Result: 8.0')

        # Test exponentiation with base zero and positive exponent
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('5', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')  # Assuming the "Exponentiate" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for exponentiation with base zero', title='Result Check', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test exponentiation with positive base and zero exponent
        pyautogui.write('7', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')  # Assuming the "Exponentiate" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for exponentiation with zero exponent', title='Result Check', default='')
        self.assertEqual(result, 'Result: 1.0')

        # Test exponentiation with negative base and even exponent
        pyautogui.write('-3', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')  # Assuming the "Exponentiate" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for exponentiation with negative base', title='Result Check', default='')
        self.assertEqual(result, 'Result: 9.0')

    def test_percentage(self):
        # Test percentage calculation
        pyautogui.write('200', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')  # Assuming the "Percentage" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for percentage', title='Result Check', default='')
        self.assertEqual(result, 'Result: 20.0')

        # Test percentage calculation with zero
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('25', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')  # Assuming the "Percentage" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for percentage with zero', title='Result Check', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test percentage calculation with negative number
        pyautogui.write('-50', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')  # Assuming the "Percentage" button is focused
        time.sleep(1)
        result = pyautogui.prompt(text='Check the result for percentage with negative number', title='Result Check', default='')
        self.assertEqual(result, 'Result: -5.0')

if __name__ == '__main__':
    unittest.main()
