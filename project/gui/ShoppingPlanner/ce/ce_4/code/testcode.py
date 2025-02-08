import unittest
from shopping_list_manager import ShoppingListManager
from item import Item

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        # Initialize the ShoppingListManager with test files
        self.manager = ShoppingListManager('test_shopping_lists.txt', 'categories.txt')
        # Clear any existing lists for a clean test environment
        self.manager.lists = {}

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.manager.create_list("Groceries")
        self.assertIn("Groceries", self.manager.lists)
        self.assertEqual(len(self.manager.lists["Groceries"]), 0)

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.manager.create_list("Groceries")
        self.manager.add_item("Groceries", "Milk", "Diary")
        items = self.manager.import_items("Groceries")
        self.assertIn(("Milk", "Diary"), items)

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.manager.create_list("Groceries")
        self.manager.add_item("Groceries", "Bread", "Bakery")
        items = self.manager.import_items("Groceries")
        self.assertIn(("Bread", "Bakery"), items)

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        # Simulate existing lists in the file
        self.manager.lists = {
            "Groceries": [Item("Milk", "Diary"), Item("Bread", "Bakery")],
            "Electronics": [Item("Laptop", "Computers")]
        }
        self.manager.create_list("NewList")
        imported_items = self.manager.import_items("Groceries")
        for item in imported_items:
            self.manager.add_item("NewList", item[0], item[1])
        new_list_items = self.manager.import_items("NewList")
        self.assertIn(("Milk", "Diary"), new_list_items)
        self.assertIn(("Bread", "Bakery"), new_list_items)

if __name__ == '__main__':
    unittest.main()
