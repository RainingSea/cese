import unittest
import json
import os
from main import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary inventory file for testing
        self.test_file_path = 'test_inventory.json'
        with open(self.test_file_path, 'w') as file:
            json.dump([], file)
        self.inventory_manager = InventoryManager(self.test_file_path)

    def tearDown(self):
        # Remove the temporary inventory file after tests
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_input_details_of_various_items(self):
        # Functionalities 1: Input Details of Various Items
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        self.assertIn({"name": "Pen", "category": "Stationery", "quantity": 100}, self.inventory_manager.items)

    def test_add_new_items_to_inventory(self):
        # Functionalities 2: Add New Items to the Inventory
        self.inventory_manager.add_item("Printer", "Electronics", 5)
        self.assertIn({"name": "Printer", "category": "Electronics", "quantity": 5}, self.inventory_manager.items)

    def test_update_stock_quantities(self):
        # Functionalities 3: Update Stock Quantities
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        self.inventory_manager.update_item("Pen", 150)
        self.assertIn({"name": "Pen", "category": "Stationery", "quantity": 150}, self.inventory_manager.items)

        self.inventory_manager.add_item("Paper", "Supplies", 200)
        self.inventory_manager.update_item("Paper", 190)
        self.assertIn({"name": "Paper", "category": "Supplies", "quantity": 190}, self.inventory_manager.items)

    def test_search_for_specific_items_in_inventory(self):
        # Functionalities 4: Search for Specific Items in the Inventory
        self.inventory_manager.add_item("Chair", "Furniture", 10)
        results = self.inventory_manager.search_item("Chair")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], {"name": "Chair", "category": "Furniture", "quantity": 10})

if __name__ == '__main__':
    unittest.main()
