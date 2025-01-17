import unittest
from receipt_manager import ReceiptManager

class TestReceiptManager(unittest.TestCase):

    def setUp(self):
        # Create a ReceiptManager instance with a test file path
        self.receipt_manager = ReceiptManager("test_receipts.txt")
        # Clear any existing data in the test file
        with open("test_receipts.txt", 'w') as file:
            file.write("")

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        
        # Check if the receipts are added correctly
        receipts = self.receipt_manager.search_receipts()
        self.assertIn(("2023-10-01", "Amazon", 150.00), receipts)
        self.assertIn(("2023-10-02", "Walmart", 75.50), receipts)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        
        # Reload receipts from file to simulate reopening the application
        self.receipt_manager.receipts = self.receipt_manager.load_receipts()
        
        # Check if the receipts are loaded correctly
        receipts = self.receipt_manager.search_receipts()
        self.assertIn(("2023-10-01", "Amazon", 150.00), receipts)
        self.assertIn(("2023-10-02", "Walmart", 75.50), receipts)

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        
        # Search by merchant
        results = self.receipt_manager.search_receipts(merchant="Amazon")
        self.assertIn(("2023-10-01", "Amazon", 150.00), results)
        
        # Search by date
        results = self.receipt_manager.search_receipts(date="2023-10-02")
        self.assertIn(("2023-10-02", "Walmart", 75.50), results)

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.receipt_manager.add_receipt("2023-10-01", "Amazon", 150.00)
        self.receipt_manager.add_receipt("2023-10-02", "Walmart", 75.50)
        
        # Search by amount
        results = self.receipt_manager.search_receipts(total_amount=150.00)
        self.assertIn(("2023-10-01", "Amazon", 150.00), results)
        
        # Search for a non-existing merchant
        results = self.receipt_manager.search_receipts(merchant="Target")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
