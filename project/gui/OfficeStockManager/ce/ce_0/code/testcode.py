import unittest
import os
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary inventory file for testing."""
        cls.test_file_path = 'test_inventory.txt'
        cls.inventory_manager = InventoryManager(cls.test_file_path)

    def setUp(self):
        """Reset the inventory file before each test."""
        with open(self.test_file_path, 'w') as f:
            f.write("Pen,Stationery,50\n")
            f.write("Notebook,Stationery,30\n")
            f.write("Stapler,Office Supplies,15\n")
        self.inventory_manager.items = self.inventory_manager.load_inventory()

    def tearDown(self):
        """Remove the test inventory file after tests."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_add_item(self):
        """Functionalities 1 & 2: Input Details of Various Items and Add New Items to the Inventory"""
        self.inventory_manager.add_item("Printer", "Electronics", 5)
        items = self.inventory_manager.load_inventory()
        self.assertIn(["Printer", "Electronics", "5"], items)

    def test_update_item(self):
        """Functionalities 3: Update Stock Quantities"""
        # Increase quantity
        self.inventory_manager.update_item("Pen", 100)
        items = self.inventory_manager.load_inventory()
        self.assertIn(["Pen", "Stationery", "100"], items)

        # Decrease quantity (this will fail if the item doesn't exist)
        self.inventory_manager.update_item("Notebook", 20)
        items = self.inventory_manager.load_inventory()
        self.assertIn(["Notebook", "Stationery", "20"], items)

    def test_search_item(self):
        """Functionalities 4: Search for Specific Items in the Inventory"""
        results = self.inventory_manager.search_item("Pen")
        self.assertEqual(results, [["Pen", "Stationery", "50"]])

        results = self.inventory_manager.search_item("Chair")
        self.assertEqual(results, [])  # No item should be found

if __name__ == '__main__':
    unittest.main()
