import unittest
import os
from main import ReceiptManager

class TestReceiptManager(unittest.TestCase):

    def setUp(self):
        # Setup a test file path
        self.test_file_path = 'test_receipts.txt'
        # Initialize the ReceiptManager with the test file
        self.receipt_manager = ReceiptManager(self.test_file_path)

    def tearDown(self):
        # Remove the test file after each test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        self.assertIn("2023-10-01,Amazon,150.0", self.receipt_manager.receipts)
        self.assertIn("2023-10-02,Walmart,75.5", self.receipt_manager.receipts)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        self.receipt_manager.load_receipts()
        self.assertIn("2023-10-01,Amazon,150.0", self.receipt_manager.receipts)
        self.assertIn("2023-10-02,Walmart,75.5", self.receipt_manager.receipts)

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        results = self.receipt_manager.search_receipts(merchant="Amazon")
        self.assertIn("2023-10-01,Amazon,150.0", results)
        results = self.receipt_manager.search_receipts(date="2023-10-02")
        self.assertIn("2023-10-02,Walmart,75.5", results)

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        results = self.receipt_manager.search_receipts(total_amount=150.00)
        self.assertIn("2023-10-01,Amazon,150.0", results)
        results = self.receipt_manager.search_receipts(merchant="Target")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
