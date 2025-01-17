import unittest
from shopping_list_manager import ShoppingListManager
from shopping_list import ShoppingList

class TestShoppingPlanner(unittest.TestCase):

    def setUp(self):
        self.manager = ShoppingListManager()

    def test_create_customizable_shopping_lists(self):
        # Functionalities 1: Create customizable shopping lists
        self.manager.create_list("Groceries")
        self.assertTrue(any(shopping_list.name == "Groceries" for shopping_list in self.manager.lists))

    def test_categorize_shopping_items(self):
        # Functionalities 2: Categorize shopping items
        self.manager.create_list("Groceries")
        self.manager.add_item("Groceries", "Milk", "Dairy")
        shopping_list = next((sl for sl in self.manager.lists if sl.name == "Groceries"), None)
        self.assertIsNotNone(shopping_list)
        self.assertTrue(any(item.name == "Milk" and item.category == "Dairy" for item in shopping_list.items))

    def test_add_items_manually_to_shopping_list(self):
        # Functionalities 3: Add items manually to the shopping list
        self.manager.create_list("Groceries")
        self.manager.add_item("Groceries", "Bread", "Bakery")
        shopping_list = next((sl for sl in self.manager.lists if sl.name == "Groceries"), None)
        self.assertIsNotNone(shopping_list)
        self.assertTrue(any(item.name == "Bread" for item in shopping_list.items))

    def test_import_items_from_previous_shopping_lists(self):
        # Functionalities 4: Import items from previous shopping lists
        self.manager.import_list('shopping_lists.txt')
        self.manager.create_list("New List")
        self.manager.add_item("New List", "Charger", "Accessories")
        shopping_list = next((sl for sl in self.manager.lists if sl.name == "New List"), None)
        self.assertIsNotNone(shopping_list)
        self.assertTrue(any(item.name == "Charger" and item.category == "Accessories" for item in shopping_list.items))

if __name__ == '__main__':
    unittest.main()
