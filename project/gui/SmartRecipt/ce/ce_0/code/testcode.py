import unittest
import subprocess
import time
import pyautogui

class TestSmartReceiptApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the application
        cls.process = subprocess.Popen(['python', 'D:/Project/CE/CE/project/gui/SmartRecipt/ce/ce_0/code/main.py'])
        time.sleep(2)  # Wait for the application to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the application
        cls.process.terminate()

    def test_input_receipt_information(self):
        # Test case for Functionality 1
        pyautogui.click(100, 100)  # Click on the date entry field
        pyautogui.typewrite('2023-10-01')
        pyautogui.press('tab')
        pyautogui.typewrite('Amazon')
        pyautogui.press('tab')
        pyautogui.typewrite('150.00')
        pyautogui.press('enter')  # Click the "Add Receipt" button
        time.sleep(1)
        # Check for success message
        success_message = pyautogui.confirm(text='Receipt added successfully!', title='Success', buttons=['OK'])
        self.assertEqual(success_message, 'OK')

        pyautogui.click(100, 100)  # Click on the date entry field
        pyautogui.typewrite('2023-10-02')
        pyautogui.press('tab')
        pyautogui.typewrite('Walmart')
        pyautogui.press('tab')
        pyautogui.typewrite('75.50')
        pyautogui.press('enter')  # Click the "Add Receipt" button
        time.sleep(1)
        # Check for success message
        success_message = pyautogui.confirm(text='Receipt added successfully!', title='Success', buttons=['OK'])
        self.assertEqual(success_message, 'OK')

    def test_store_and_organize_receipts(self):
        # Test case for Functionality 2
        # This test assumes the application is closed and reopened
        # Check if receipts are stored and displayed correctly
        with open('D:/Project/CE/CE/project/gui/SmartRecipt/ce/ce_0/code/receipts.txt', 'r') as file:
            receipts = file.readlines()
        self.assertIn('2023-10-01,Amazon,150.00\n', receipts)
        self.assertIn('2023-10-02,Walmart,75.50\n', receipts)

    def test_search_for_specific_receipts(self):
        # Test case for Functionality 3
        pyautogui.click(100, 200)  # Click on the search entry field
        pyautogui.typewrite('Amazon')
        pyautogui.press('enter')  # Click the "Search" button
        time.sleep(1)
        # Verify search results
        search_results = pyautogui.confirm(text='2023-10-01,Amazon,150.00', title='Search Results', buttons=['OK'])
        self.assertEqual(search_results, 'OK')

        pyautogui.click(100, 200)  # Click on the search entry field
        pyautogui.typewrite('2023-10-02')
        pyautogui.press('enter')  # Click the "Search" button
        time.sleep(1)
        # Verify search results
        search_results = pyautogui.confirm(text='2023-10-02,Walmart,75.50', title='Search Results', buttons=['OK'])
        self.assertEqual(search_results, 'OK')

    def test_retrieve_specific_receipts(self):
        # Test case for Functionality 4
        pyautogui.click(100, 200)  # Click on the search entry field
        pyautogui.typewrite('150.00')
        pyautogui.press('enter')  # Click the "Search" button
        time.sleep(1)
        # Verify search results
        search_results = pyautogui.confirm(text='2023-10-01,Amazon,150.00', title='Search Results', buttons=['OK'])
        self.assertEqual(search_results, 'OK')

        pyautogui.click(100, 200)  # Click on the search entry field
        pyautogui.typewrite('Target')
        pyautogui.press('enter')  # Click the "Search" button
        time.sleep(1)
        # Verify no results found
        no_results_message = pyautogui.confirm(text='No receipts found matching the search criteria.', title='Search Results', buttons=['OK'])
        self.assertEqual(no_results_message, 'OK')

if __name__ == '__main__':
    unittest.main()
