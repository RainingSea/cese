import unittest
import os
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Set up a test inventory file
        self.test_file_path = 'test_inventory.txt'
        with open(self.test_file_path, 'w') as file:
            file.write("Paper,Stationery,100\nPens,Stationery,200\nStapler,Stationery,50\nNotebook,Stationery,150\n")
        self.inventory_manager = InventoryManager(self.test_file_path)

    def tearDown(self):
        # Remove the test inventory file after tests
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_input_details_of_various_items(self):
        # Functionalities 1: Input Details of Various Items
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        item = self.inventory_manager.search_item("Pen")
        self.assertEqual(item['item_name'], "Pen")
        self.assertEqual(item['item_type'], "Stationery")
        self.assertEqual(item['quantity'], 100)

    def test_add_new_items_to_inventory(self):
        # Functionalities 2: Add New Items to the Inventory
        self.inventory_manager.add_item("Printer", "Electronics", 5)
        item = self.inventory_manager.search_item("Printer")
        self.assertEqual(item['item_name'], "Printer")
        self.assertEqual(item['item_type'], "Electronics")
        self.assertEqual(item['quantity'], 5)

    def test_update_stock_quantities(self):
        # Functionalities 3: Update Stock Quantities
        # Increase quantity
        self.inventory_manager.update_quantity("Pens", 250)
        item = self.inventory_manager.search_item("Pens")
        self.assertEqual(item['quantity'], 250)

        # Decrease quantity
        self.inventory_manager.update_quantity("Paper", 90)
        item = self.inventory_manager.search_item("Paper")
        self.assertEqual(item['quantity'], 90)

    def test_search_for_specific_items(self):
        # Functionalities 4: Search for Specific Items in the Inventory
        item = self.inventory_manager.search_item("Chair")
        self.assertEqual(item, {})  # Expecting an empty dictionary as "Chair" does not exist

if __name__ == '__main__':
    unittest.main()
