import unittest
import pyautogui
import time
import subprocess

class TestCalculationAssistant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Calculation Assistant application
        cls.process = subprocess.Popen(["python", "D:/Project/CE/CE/project/gui/CalculationAssistant/ce/ce_0/code/main.py"])
        time.sleep(2)  # Wait for the GUI to initialize

    @classmethod
    def tearDownClass(cls):
        # Terminate the Calculation Assistant application
        cls.process.terminate()

    def test_basic_arithmetic_operations(self):
        # Test addition
        pyautogui.write('5', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('3', interval=0.1)
        pyautogui.press('tab', presses=2)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 8.0')

        # Test subtraction
        pyautogui.write('7', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('-2', interval=0.1)
        pyautogui.press('tab', presses=3)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 9.0')

        # Test multiplication
        pyautogui.write('4', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('6', interval=0.1)
        pyautogui.press('tab', presses=4)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 24.0')

        # Test division
        pyautogui.write('8', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab', presses=5)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 4.0')

        # Test division by zero
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab', presses=5)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertIn('Cannot divide by zero', result)

    def test_square_root(self):
        # Test square root of positive number
        pyautogui.write('16', interval=0.1)
        pyautogui.press('tab')
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 4.0')

        # Test square root of zero
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab')
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test square root of negative number
        pyautogui.write('-9', interval=0.1)
        pyautogui.press('tab')
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertIn('Invalid input for square root', result)

    def test_exponentiation(self):
        # Test exponentiation with positive base and exponent
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('3', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 8.0')

        # Test exponentiation with base zero and positive exponent
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('5', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test exponentiation with positive base and zero exponent
        pyautogui.write('7', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 1.0')

        # Test exponentiation with negative base and even exponent
        pyautogui.write('-3', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('2', interval=0.1)
        pyautogui.press('tab', presses=7)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 9.0')

    def test_calculate_percentage(self):
        # Test percentage calculation with positive number
        pyautogui.write('200', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 20.0')

        # Test percentage calculation with zero
        pyautogui.write('0', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('25', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: 0.0')

        # Test percentage calculation with negative number
        pyautogui.write('-50', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('10', interval=0.1)
        pyautogui.press('tab', presses=8)
        pyautogui.press('enter')
        time.sleep(1)
        result = pyautogui.prompt(text='', title='Result', default='')
        self.assertEqual(result, 'Result: -5.0')

if __name__ == '__main__':
    unittest.main()
