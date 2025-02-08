import unittest
from shopping_planner import ShoppingPlanner

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ShoppingPlanner()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.planner.create_shopping_list("Weekend Shopping")
        self.assertIn("Weekend Shopping", self.planner.shopping_lists)
        self.assertEqual(self.planner.shopping_lists["Weekend Shopping"], [])

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.planner.create_shopping_list("Weekend Shopping")
        self.planner.add_item_to_list("Weekend Shopping", "Milk", "Grocery")
        self.assertIn("Grocery|Milk", self.planner.shopping_lists["Weekend Shopping"])

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.planner.create_shopping_list("Weekend Shopping")
        self.planner.add_item_to_list("Weekend Shopping", "Bread", "Grocery")
        self.assertIn("Grocery|Bread", self.planner.shopping_lists["Weekend Shopping"])

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        self.planner.create_shopping_list("Old List")
        self.planner.add_item_to_list("Old List", "Eggs", "Grocery")
        self.planner.create_shopping_list("New List")
        self.planner.import_items_from_list("New List", "Old List")
        self.assertIn("Grocery|Eggs", self.planner.shopping_lists["New List"])

if __name__ == '__main__':
    unittest.main()
