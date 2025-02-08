import unittest
import tkinter as tk
from shopping_list import ShoppingList
from main import MainApp

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MainApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.app.create_list()
        self.assertEqual(len(self.app.current_list.get_items()), 0, "New list should be empty")

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.app.entry_name.insert(0, "Apple")
        self.app.entry_category.insert(0, "Groceries")
        self.app.add_item()
        items = self.app.current_list.get_items()
        self.assertIn(("Apple", "Groceries"), items, "Item should be added with correct category")

    def test_add_items_manually_to_the_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.app.entry_name.insert(0, "Banana")
        self.app.entry_category.insert(0, "Fruits")
        self.app.add_item()
        items = self.app.current_list.get_items()
        self.assertIn(("Banana", "Fruits"), items, "Item should be added manually to the list")

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        self.app.current_list.import_items('previous_lists.txt')
        items = self.app.current_list.get_items()
        expected_items = [("milk", "dairy"), ("bread", "grains"), ("eggs", "protein")]
        for item in expected_items:
            self.assertIn(item, items, f"Item {item} should be imported from previous list")

if __name__ == '__main__':
    unittest.main()
