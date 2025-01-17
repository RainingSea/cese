import unittest
import os
import shutil
from tkinter import Tk
from main import Main
from ReceiptManager import ReceiptManager

class TestSmartReceiptApp(unittest.TestCase):

    def setUp(self):
        # Set up the test environment
        self.test_dir = 'test_receipts'
        self.receipt_manager = ReceiptManager(file_path=self.test_dir)
        self.root = Tk()
        self.app = Main(self.root)
        self.app.receipt_manager = self.receipt_manager

    def tearDown(self):
        # Clean up the test environment
        self.root.destroy()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_input_receipt_information(self):
        # Functionality 1: Input Receipt Information
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()
        
        self.app.date_entry.delete(0, 'end')
        self.app.merchant_entry.delete(0, 'end')
        self.app.amount_entry.delete(0, 'end')
        
        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        receipts = self.receipt_manager.load_receipts()
        self.assertIn("2023-10-01,Amazon,150.0", receipts)
        self.assertIn("2023-10-02,Walmart,75.5", receipts)

    def test_store_and_organize_receipts(self):
        # Functionality 2: Store and Organize Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()
        
        self.app.date_entry.delete(0, 'end')
        self.app.merchant_entry.delete(0, 'end')
        self.app.amount_entry.delete(0, 'end')
        
        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        # Simulate closing and reopening the application
        self.tearDown()
        self.setUp()

        receipts = self.receipt_manager.load_receipts()
        self.assertIn("2023-10-01,Amazon,150.0", receipts)
        self.assertIn("2023-10-02,Walmart,75.5", receipts)

    def test_search_for_specific_receipts(self):
        # Functionality 3: Search for Specific Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()
        
        self.app.date_entry.delete(0, 'end')
        self.app.merchant_entry.delete(0, 'end')
        self.app.amount_entry.delete(0, 'end')
        
        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        self.app.search_entry.insert(0, "Amazon")
        self.app.search_receipts()
        search_results = self.app.results_listbox.get(0, 'end')
        self.assertIn("2023-10-01,Amazon,150.0", search_results)

        self.app.search_entry.delete(0, 'end')
        self.app.search_entry.insert(0, "2023-10-02")
        self.app.search_receipts()
        search_results = self.app.results_listbox.get(0, 'end')
        self.assertIn("2023-10-02,Walmart,75.5", search_results)

    def test_retrieve_specific_receipts(self):
        # Functionality 4: Retrieve Specific Receipts
        self.app.date_entry.insert(0, "2023-10-01")
        self.app.merchant_entry.insert(0, "Amazon")
        self.app.amount_entry.insert(0, "150.00")
        self.app.save_receipt()
        
        self.app.date_entry.delete(0, 'end')
        self.app.merchant_entry.delete(0, 'end')
        self.app.amount_entry.delete(0, 'end')
        
        self.app.date_entry.insert(0, "2023-10-02")
        self.app.merchant_entry.insert(0, "Walmart")
        self.app.amount_entry.insert(0, "75.50")
        self.app.save_receipt()

        self.app.search_entry.insert(0, "150.00")
        self.app.search_receipts()
        search_results = self.app.results_listbox.get(0, 'end')
        self.assertIn("2023-10-01,Amazon,150.0", search_results)

        self.app.search_entry.delete(0, 'end')
        self.app.search_entry.insert(0, "Target")
        self.app.search_receipts()
        search_results = self.app.results_listbox.get(0, 'end')
        self.assertEqual(len(search_results), 0)

if __name__ == '__main__':
    unittest.main()
