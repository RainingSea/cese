import unittest
import os
from main import Main
from search_engine import SearchEngine

class TestSmartReceipt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a SearchEngine instance for testing
        cls.search_engine = SearchEngine()

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.search_engine.add_receipt("2023-10-01", "Amazon", 150.00)
        self.assertIn("2023-10-01,Amazon,150.0", self.search_engine.receipts)

        self.search_engine.add_receipt("2023-10-02", "Walmart", 75.50)
        self.assertIn("2023-10-02,Walmart,75.5", self.search_engine.receipts)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.search_engine.add_receipt("2023-10-03", "Starbucks", 5.75)
        self.assertIn("2023-10-03,Starbucks,5.75", self.search_engine.receipts)

        # Simulate closing and reopening the application
        self.search_engine = SearchEngine()  # Reload receipts
        self.assertIn("2023-10-01,Amazon,150.0", self.search_engine.receipts)
        self.assertIn("2023-10-02,Walmart,75.5", self.search_engine.receipts)
        self.assertIn("2023-10-03,Starbucks,5.75", self.search_engine.receipts)

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.search_engine.add_receipt("2023-10-01", "Amazon", 150.00)
        self.search_engine.add_receipt("2023-10-02", "Walmart", 75.50)

        results_amazon = self.search_engine.search_receipts("Amazon")
        self.assertIn("2023-10-01,Amazon,150.0", results_amazon)

        results_walmart = self.search_engine.search_receipts("2023-10-02")
        self.assertIn("2023-10-02,Walmart,75.5", results_walmart)

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.search_engine.add_receipt("2023-10-01", "Amazon", 150.00)
        self.search_engine.add_receipt("2023-10-02", "Walmart", 75.50)

        results_amount = self.search_engine.search_receipts("150.00")
        self.assertIn("2023-10-01,Amazon,150.0", results_amount)

        results_no_match = self.search_engine.search_receipts("Target")
        self.assertEqual(results_no_match, [])

    @classmethod
    def tearDownClass(cls):
        # Clean up the receipts file after tests
        if os.path.exists('receipts.txt'):
            os.remove('receipts.txt')

if __name__ == '__main__':
    unittest.main()
