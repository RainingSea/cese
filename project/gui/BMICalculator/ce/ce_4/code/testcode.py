import unittest
import pyautogui
import time
import os

class TestBMICalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the application
        os.system("start python D:/Project/CE/CE/project/gui/BMICalculator/ce/ce_4/code/main.py")
        time.sleep(2)  # Wait for the application to start

    def test_user_input(self):
        # Functionality 1: User Input for Weight and Height
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for no error message
        self.assertNotIn("Input error", pyautogui.getActiveWindow().title)

        # Test invalid input
        pyautogui.write('-70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('0', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for error message
        self.assertIn("Input error", pyautogui.getActiveWindow().title)

    def test_calculate_bmi(self):
        # Functionality 2: Calculate BMI
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct BMI calculation
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("BMI: 22.86", result_text)

        pyautogui.write('50', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.60', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct BMI calculation
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("BMI: 19.53", result_text)

    def test_classify_bmi(self):
        # Functionality 3: Classify BMI
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct classification
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Classification: Normal weight", result_text)

        pyautogui.write('90', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct classification
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Classification: Overweight", result_text)

    def test_view_interpretation(self):
        # Functionality 4: View Interpretation of BMI
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct interpretation
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Interpretation: You are within the healthy weight range.", result_text)

        pyautogui.write('50', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.70', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct interpretation
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Interpretation: You are under the healthy weight range.", result_text)

    def test_provide_recommendations(self):
        # Functionality 5: Provide BMI Recommendations
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct recommendations
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Recommendations: Maintain your current lifestyle.", result_text)

        pyautogui.write('95', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check for correct recommendations
        result_text = pyautogui.getActiveWindow().children()[0].text
        self.assertIn("Recommendations: Seek medical advice for weight management.", result_text)

    def test_data_storage(self):
        # Functionality 6: Data Storage
        pyautogui.write('70', interval=0.1)
        pyautogui.press('tab')
        pyautogui.write('1.75', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)
        # Check if the data is saved correctly
        with open('D:/Project/CE/CE/project/gui/BMICalculator/ce/ce_4/code/bmi_results.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn("70|1.75|22.86|Normal weight|You are within the healthy weight range.|Maintain your current lifestyle.\n", lines)

    @classmethod
    def tearDownClass(cls):
        # Close the application
        pyautogui.hotkey('alt', 'f4')

if __name__ == '__main__':
    unittest.main()
