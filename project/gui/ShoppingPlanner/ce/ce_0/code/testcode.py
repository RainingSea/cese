import unittest
import os
from main import Main
from shopping_list_manager import ShoppingListManager

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.manager = self.app.shopping_list_manager

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.manager.create_list()  # Create a new shopping list
        self.assertEqual(self.manager.get_items(), [])  # Expecting an empty list

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.manager.create_list()
        self.manager.add_item("Milk", "Dairy")
        self.assertIn("Milk|Dairy", self.manager.get_items())  # Expecting the item to be added

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.manager.create_list()
        self.manager.add_item("Bread", "Bakery")
        self.assertIn("Bread|Bakery", self.manager.get_items())  # Expecting the item to be added

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        self.manager.create_list()
        # Create a temporary shopping list file for testing
        with open('test_shopping_list.txt', 'w') as f:
            f.write("Eggs|Dairy\n")
            f.write("Apples|Fruits\n")
        
        self.manager.import_items('test_shopping_list.txt')
        self.assertIn("Eggs|Dairy", self.manager.get_items())  # Expecting the item to be imported
        self.assertIn("Apples|Fruits", self.manager.get_items())  # Expecting the item to be imported

        # Clean up the test file
        os.remove('test_shopping_list.txt')

if __name__ == '__main__':
    unittest.main()
