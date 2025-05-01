import unittest
import os
from tkinter import Tk
from main import Main, ShoppingList

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = Main(self.root)
        self.app.current_list = ShoppingList()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.fail("not implemented")  # Functionality to create a unique shopping list by name is not implemented

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.app.item_entry.insert(0, "Milk")
        self.app.category_entry.insert(0, "Dairy")
        self.app.add_item()
        self.assertIn("Milk (Dairy)", self.app.listbox.get(0))  # Check if the item is added with the category

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.app.item_entry.insert(0, "Bread")
        self.app.add_item()
        self.assertIn("Bread", self.app.listbox.get(0))  # Check if the item is added successfully

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        self.app.import_previous_list()
        self.assertIn("Milk (Dairy)", self.app.listbox.get(0))  # Check if the item from previous list is imported
        self.assertIn("Eggs (Dairy)", self.app.listbox.get(1))  # Check if the item from previous list is imported
        self.assertIn("Bread (Grains)", self.app.listbox.get(2))  # Check if the item from previous list is imported

    def tearDown(self):
        self.root.destroy()
        # Clean up the shopping_lists.txt file after tests
        if os.path.exists('shopping_lists.txt'):
            os.remove('shopping_lists.txt')

if __name__ == '__main__':
    unittest.main()
