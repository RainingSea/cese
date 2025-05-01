import unittest
import os
from tkinter import Tk
from main import Main, Receipt

class TestSmartReceipt(unittest.TestCase):

    def setUp(self):
        # Create a temporary Tkinter root window for testing
        self.root = Tk()
        self.app = Main(self.root)
        self.app.receipts = []  # Clear receipts for testing

    def tearDown(self):
        # Close the Tkinter window after tests
        self.root.destroy()
        # Remove the receipts file if it exists
        if os.path.exists('receipts.txt'):
            os.remove('receipts.txt')

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()

        self.assertEqual(len(self.app.receipts), 1)
        self.assertEqual(self.app.receipts[0].date, "2023-10-01")
        self.assertEqual(self.app.receipts[0].merchant, "Amazon")
        self.assertEqual(self.app.receipts[0].total_amount, 150.00)

        self.app.date_entry.delete(0, 'end')
        self.app.merchant_entry.delete(0, 'end')
        self.app.amount_entry.delete(0, 'end')

        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        self.assertEqual(len(self.app.receipts), 2)
        self.assertEqual(self.app.receipts[1].date, "2023-10-02")
        self.assertEqual(self.app.receipts[1].merchant, "Walmart")
        self.assertEqual(self.app.receipts[1].total_amount, 75.50)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()

        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        # Close and reopen the application
        self.app.save_receipts_to_file()
        self.app.receipts = self.app.load_receipts()

        self.assertEqual(len(self.app.receipts), 2)
        self.assertEqual(self.app.receipts[0].merchant, "Amazon")
        self.assertEqual(self.app.receipts[1].merchant, "Walmart")

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()

        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        # Search for "Amazon"
        self.app.search_entry.insert(0, "Amazon")
        self.app.search_receipts(self.app.search_entry.get())
        self.assertIn("2023-10-01, Amazon, 150.0", self.app.results_text.get(1.0, 'end'))

        # Search for "2023-10-02"
        self.app.search_entry.delete(0, 'end')
        self.app.search_entry.insert(0, "2023-10-02")
        self.app.search_receipts(self.app.search_entry.get())
        self.assertIn("2023-10-02, Walmart, 75.5", self.app.results_text.get(1.0, 'end'))

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()

        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        # Search for total amount "150.00"
        self.app.search_entry.insert(0, "150.00")
        self.app.search_receipts(self.app.search_entry.get())
        self.assertIn("2023-10-01, Amazon, 150.0", self.app.results_text.get(1.0, 'end'))

        # Search for a non-existing merchant "Target"
        self.app.search_entry.delete(0, 'end')
        self.app.search_entry.insert(0, "Target")
        self.app.search_receipts(self.app.search_entry.get())
        self.assertIn("No receipts found.", self.app.results_text.get(1.0, 'end'))

if __name__ == '__main__':
    unittest.main()
