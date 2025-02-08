import unittest
from shopping_list_manager import ShoppingListManager
from shopping_list import ShoppingList

class TestShoppingListManager(unittest.TestCase):

    def setUp(self):
        self.manager = ShoppingListManager()
        self.manager.load_lists()

    def test_create_and_manage_shopping_lists(self):
        # Functionality 1: Create and Manage Shopping Lists
        initial_count = len(self.manager.list_of_lists)

        # Create a new list
        self.manager.create_list("Test List")
        self.assertIn("Test List", self.manager.list_of_lists)
        self.assertEqual(len(self.manager.list_of_lists), initial_count + 1)

        # Delete the newly created list
        self.manager.delete_list("Test List")
        self.assertNotIn("Test List", self.manager.list_of_lists)
        self.assertEqual(len(self.manager.list_of_lists), initial_count)

    def test_add_and_categorize_items_in_the_list(self):
        # Functionality 2: Add and Categorize Items in the List
        self.manager.create_list("Test List")
        test_list = self.manager.list_of_lists["Test List"]

        # Add item "Milk" under "Dairy"
        test_list.add_item("Milk", "Dairy")
        self.assertIn({'item': 'Milk', 'category': 'Dairy'}, test_list.items)

        # Add item "Bread" under "Bakery"
        test_list.add_item("Bread", "Bakery")
        self.assertIn({'item': 'Bread', 'category': 'Bakery'}, test_list.items)

    def test_set_reminders_for_upcoming_shopping_trips(self):
        # Functionality 3: Set Reminders for Upcoming Shopping Trips
        self.manager.create_list("Test List")
        test_list = self.manager.list_of_lists["Test List"]

        # Set a reminder
        test_list.set_reminder("2023-12-25", "10:00 AM")
        self.assertEqual(test_list.reminder, {'date': "2023-12-25", 'time': "10:00 AM"})

    def test_intuitive_and_simple_user_interface(self):
        # Functionality 4: Intuitive and Simple User Interface for Easy Navigation
        # This functionality is related to GUI navigation and help dialog.
        # Since the current codebase does not implement these features, we will mark this test as a failure.
        self.fail("GUI navigation and help dialog functionality not implemented")

if __name__ == '__main__':
    unittest.main()
