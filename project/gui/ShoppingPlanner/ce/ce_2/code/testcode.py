import unittest
import os
from main import ShoppingList

class TestShoppingList(unittest.TestCase):

    def setUp(self):
        self.shopping_list = ShoppingList()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        # This functionality is not implemented in the codebase, so we will fail the test.
        self.fail("Create customizable shopping lists functionality not implemented.")

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.shopping_list.add_item("Milk", "Dairy")
        self.assertIn(("Milk", "Dairy"), self.shopping_list.items)
        self.assertIn("Dairy", self.shopping_list.categories)

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.shopping_list.add_item("Bread", "Bakery")
        self.assertIn(("Bread", "Bakery"), self.shopping_list.items)

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        # Create a temporary file to simulate importing items
        test_file_path = 'test_shopping_list.txt'
        with open(test_file_path, 'w') as f:
            f.write("Eggs|Dairy\n")
            f.write("Fruits|Produce\n")

        self.shopping_list.import_items(test_file_path)
        self.assertIn(("Eggs", "Dairy"), self.shopping_list.items)
        self.assertIn(("Fruits", "Produce"), self.shopping_list.items)

        # Clean up the test file
        os.remove(test_file_path)

if __name__ == '__main__':
    unittest.main()
