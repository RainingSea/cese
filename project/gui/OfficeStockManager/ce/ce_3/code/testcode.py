import unittest
from inventory_manager import InventoryManager
from item import Item

class TestOfficeStockManager(unittest.TestCase):

    def setUp(self):
        self.inventory_manager = InventoryManager()
        self.inventory_manager.load_inventory('inventory.json')

    def test_input_details_of_various_items(self):
        # Functionalities 1: Input Details of Various Items
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        item = next((item for item in self.inventory_manager.items if item.name == "Pen"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Pen")
        self.assertEqual(item.category, "Stationery")
        self.assertEqual(item.quantity, 100)

    def test_add_new_items_to_inventory(self):
        # Functionalities 2: Add New Items to the Inventory
        self.inventory_manager.add_item("Printer", "Electronics", 5)
        item = next((item for item in self.inventory_manager.items if item.name == "Printer"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Printer")
        self.assertEqual(item.category, "Electronics")
        self.assertEqual(item.quantity, 5)

    def test_update_stock_quantities(self):
        # Functionalities 3: Update Stock Quantities
        # Increase quantity
        self.inventory_manager.add_item("Pen", "Stationery", 100)
        self.inventory_manager.update_item("Pen", 150)
        item = next((item for item in self.inventory_manager.items if item.name == "Pen"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item.quantity, 150)

        # Decrease quantity
        self.inventory_manager.add_item("Paper", "Stationery", 100)
        self.inventory_manager.update_item("Paper", 90)
        item = next((item for item in self.inventory_manager.items if item.name == "Paper"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item.quantity, 90)

    def test_search_for_specific_items(self):
        # Functionalities 4: Search for Specific Items in the Inventory
        self.inventory_manager.add_item("Chair", "Furniture", 10)
        results = self.inventory_manager.search_item("Chair")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Chair")
        self.assertEqual(results[0].category, "Furniture")
        self.assertEqual(results[0].quantity, 10)

if __name__ == '__main__':
    unittest.main()
