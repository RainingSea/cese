import unittest
import os
from main import ReceiptManager

class TestReceiptManager(unittest.TestCase):

    def setUp(self):
        self.receipt_manager = ReceiptManager()
        # Clear the receipts file before each test
        if os.path.exists('receipts.txt'):
            os.remove('receipts.txt')

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.assertIn("2023-10-01,Amazon,150.0", self.receipt_manager.receipts)
        
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        self.assertIn("2023-10-02,Walmart,75.5", self.receipt_manager.receipts)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        
        # Check if receipts are stored in the file
        self.receipt_manager.save_receipts()
        self.receipt_manager.load_receipts()
        self.assertEqual(len(self.receipt_manager.receipts), 2)

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)

        results = self.receipt_manager.search_receipts("Amazon")
        self.assertIn("2023-10-01,Amazon,150.0", results)

        results = self.receipt_manager.search_receipts("2023-10-02")
        self.assertIn("2023-10-02,Walmart,75.5", results)

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)

        results = self.receipt_manager.search_receipts("150.00")
        self.assertIn("2023-10-01,Amazon,150.0", results)

        results = self.receipt_manager.search_receipts("Target")
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
