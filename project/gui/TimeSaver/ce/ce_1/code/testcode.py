import unittest
import os
from shopping_list_manager import ShoppingListManager
from shopping_list import ShoppingList
from reminder import Reminder

class TestTimeSaver(unittest.TestCase):

    def setUp(self):
        # Setup for ShoppingListManager
        self.manager = ShoppingListManager()
        self.test_list_name = "test_list"
        self.manager.create_list(self.test_list_name)

        # Setup for ShoppingList
        self.shopping_list = ShoppingList(self.test_list_name)

        # Setup for Reminder
        self.reminder = Reminder("2023-10-01 10:00")

    def tearDown(self):
        # Clean up created test files
        if self.test_list_name in self.manager.list_files:
            self.manager.delete_list(self.test_list_name)

    def test_create_and_manage_shopping_lists(self):
        # Functionalities 1: Create and Manage Shopping Lists
        self.assertIn(self.test_list_name, self.manager.load_lists())

        # Delete the list and check
        self.manager.delete_list(self.test_list_name)
        self.assertNotIn(self.test_list_name, self.manager.load_lists())

    def test_add_and_categorize_items_in_the_list(self):
        # Functionalities 2: Add and Categorize Items in the List
        self.shopping_list.add_item("Milk", "Dairy")
        self.shopping_list.add_item("Bread", "Bakery")

        items = self.shopping_list.get_items()
        self.assertIn(("Milk", "Dairy"), items)
        self.assertIn(("Bread", "Bakery"), items)

    def test_set_reminders_for_upcoming_shopping_trips(self):
        # Functionalities 3: Set Reminders for Upcoming Shopping Trips
        self.reminder.set_reminder("2023-10-02 15:30")
        reminders = self.reminder.get_reminders()
        self.assertIn("2023-10-02 15:30", reminders)

    def test_intuitive_and_simple_user_interface(self):
        # Functionalities 4: Intuitive and Simple User Interface for Easy Navigation
        # Since we cannot test GUI directly, we will simulate the logic
        # This test will always fail as GUI testing is not implemented
        self.fail("GUI testing not implemented")

if __name__ == '__main__':
    unittest.main()
