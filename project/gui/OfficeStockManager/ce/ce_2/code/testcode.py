import unittest
import os
from inventory_manager import InventoryManager
from item import Item

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary inventory file for testing
        self.test_filename = 'test_inventory.txt'
        self.inventory_manager = InventoryManager()
        self.inventory_manager.data_handler.filename = self.test_filename
        self.inventory_manager.items = []  # Clear any existing items

    def tearDown(self):
        # Remove the test inventory file after tests
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_item(self):
        # Functionalities 1 & 2: Input Details of Various Items and Add New Items to the Inventory
        self.inventory_manager.add_item("Pen", "Stationery", 100, "Blue ink pens")
        self.assertEqual(len(self.inventory_manager.items), 1)
        self.assertEqual(self.inventory_manager.items[0].name, "Pen")
        self.assertEqual(self.inventory_manager.items[0].category, "Stationery")
        self.assertEqual(self.inventory_manager.items[0].quantity, 100)
        self.assertEqual(self.inventory_manager.items[0].description, "Blue ink pens")

        # Adding another item
        self.inventory_manager.add_item("Printer", "Electronics", 5, "Laser printer")
        self.assertEqual(len(self.inventory_manager.items), 2)
        self.assertEqual(self.inventory_manager.items[1].name, "Printer")

    def test_update_quantity(self):
        # Functionalities 3: Update Stock Quantities
        self.inventory_manager.add_item("Pen", "Stationery", 100, "Blue ink pens")
        
        # Increase quantity
        self.inventory_manager.update_quantity("Pen", 50)
        self.assertEqual(self.inventory_manager.items[0].quantity, 150)

        # Decrease quantity
        self.inventory_manager.update_quantity("Pen", -50)
        self.assertEqual(self.inventory_manager.items[0].quantity, 100)

        # Attempt to decrease quantity of a non-existing item
        self.inventory_manager.update_quantity("Paper", -10)  # Should not affect anything
        self.assertEqual(self.inventory_manager.items[0].quantity, 100)

    def test_search_item(self):
        # Functionalities 4: Search for Specific Items in the Inventory
        self.inventory_manager.add_item("Chair", "Furniture", 10, "Office chair")
        
        # Search for existing item
        item = self.inventory_manager.search_item("Chair")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Chair")
        
        # Search for non-existing item
        item = self.inventory_manager.search_item("Table")
        self.assertIsNone(item)

if __name__ == '__main__':
    unittest.main()
