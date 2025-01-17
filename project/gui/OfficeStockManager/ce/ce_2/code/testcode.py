import unittest
import os
import json
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary inventory file for testing
        self.test_inventory_file = 'test_inventory.json'
        with open(self.test_inventory_file, 'w') as file:
            json.dump([], file)
        self.inventory_manager = InventoryManager(self.test_inventory_file)

    def tearDown(self):
        # Remove the temporary inventory file after tests
        if os.path.exists(self.test_inventory_file):
            os.remove(self.test_inventory_file)

    def test_input_details_of_various_items(self):
        # Functionalities 1: Input Details of Various Items
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        item = self.inventory_manager.search_item("Pen")
        self.assertEqual(item['name'], "Pen")
        self.assertEqual(item['category'], "Stationery")
        self.assertEqual(item['quantity'], 100)

    def test_add_new_items_to_inventory(self):
        # Functionalities 2: Add New Items to the Inventory
        self.inventory_manager.add_item("Printer", "Electronics", 5)
        item = self.inventory_manager.search_item("Printer")
        self.assertEqual(item['name'], "Printer")
        self.assertEqual(item['category'], "Electronics")
        self.assertEqual(item['quantity'], 5)

    def test_update_stock_quantities(self):
        # Functionalities 3: Update Stock Quantities
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        
        # Increase quantity
        self.inventory_manager.update_item("Pen", 150)
        item = self.inventory_manager.search_item("Pen")
        self.assertEqual(item['quantity'], 150)

        # Decrease quantity
        self.inventory_manager.add_item("Paper", "Stationery", 100)
        self.inventory_manager.update_item("Paper", 90)
        item = self.inventory_manager.search_item("Paper")
        self.assertEqual(item['quantity'], 90)

    def test_search_for_specific_items_in_inventory(self):
        # Functionalities 4: Search for Specific Items in the Inventory
        self.inventory_manager.add_item("Chair", "Furniture", 10)
        item = self.inventory_manager.search_item("Chair")
        self.assertEqual(item['name'], "Chair")
        self.assertEqual(item['category'], "Furniture")
        self.assertEqual(item['quantity'], 10)

if __name__ == '__main__':
    unittest.main()
