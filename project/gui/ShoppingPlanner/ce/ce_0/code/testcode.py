import unittest
import os
from main import ShoppingPlanner, ShoppingList

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        # Setup a ShoppingPlanner instance for testing
        self.planner = ShoppingPlanner()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        initial_count = len(self.planner.list_of_lists)
        self.planner.create_shopping_list()
        # Simulate user input for the dialog
        self.planner.list_of_lists[-1].name = "Test List"
        self.assertEqual(len(self.planner.list_of_lists), initial_count + 1)
        self.assertEqual(self.planner.list_of_lists[-1].name, "Test List")

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        shopping_list = ShoppingList("Test List")
        shopping_list.add_item("Milk", "Groceries")
        self.assertIn("Groceries", shopping_list.items)
        self.assertIn("Milk", shopping_list.items["Groceries"])

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        shopping_list = ShoppingList("Test List")
        shopping_list.add_item("Bread", "Bakery")
        self.assertIn("Bakery", shopping_list.items)
        self.assertIn("Bread", shopping_list.items["Bakery"])

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        previous_items = [("Apples", "Fruits"), ("Charger", "Electronics")]
        shopping_list = ShoppingList("Test List")
        shopping_list.import_items(previous_items)
        self.assertIn("Fruits", shopping_list.items)
        self.assertIn("Apples", shopping_list.items["Fruits"])
        self.assertIn("Electronics", shopping_list.items)
        self.assertIn("Charger", shopping_list.items["Electronics"])

if __name__ == '__main__':
    unittest.main()
