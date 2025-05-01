import unittest
import os
from main import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.manager = InventoryManager()
        # Clear the inventory file before each test
        self.manager.save_inventory()

    def test_add_item(self):
        # Functionalities 1: Input Details of Various Items
        self.manager.add_item("Pen", "Stationery", 100)
        self.assertEqual(len(self.manager.items), 1)
        self.assertEqual(self.manager.items[0].name, "Pen")
        self.assertEqual(self.manager.items[0].category, "Stationery")
        self.assertEqual(self.manager.items[0].quantity, 100)

        # Functionalities 2: Add New Items to the Inventory
        self.manager.add_item("Printer", "Electronics", 5)
        self.assertEqual(len(self.manager.items), 2)
        self.assertEqual(self.manager.items[1].name, "Printer")
        self.assertEqual(self.manager.items[1].category, "Electronics")
        self.assertEqual(self.manager.items[1].quantity, 5)

    def test_update_item(self):
        # Add initial items
        self.manager.add_item("Pen", "Stationery", 100)
        self.manager.add_item("Paper", "Office Supplies", 100)

        # Increase stock quantity
        self.manager.update_item("Pen", 150)
        self.assertEqual(self.manager.items[0].quantity, 150)

        # Decrease stock quantity
        self.manager.update_item("Paper", 90)
        self.assertEqual(self.manager.items[1].quantity, 90)

        # Attempt to update a non-existent item
        with self.assertRaises(Exception):
            self.manager.update_item("NonExistentItem", 50)

    def test_search_item(self):
        # Add initial items
        self.manager.add_item("Pen", "Stationery", 100)
        self.manager.add_item("Paper", "Office Supplies", 100)

        # Search for an existing item
        results = self.manager.search_item("Pen")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Pen")

        # Search for a non-existent item
        results = self.manager.search_item("Chair")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
