import unittest
import tkinter as tk
from main import Main
from ShoppingListManager import ShoppingListManager

class TestTimeSaverApp(unittest.TestCase):

    def setUp(self):
        # Set up the Tkinter root and the application
        self.root = tk.Tk()
        self.app = Main(self.root)

    def tearDown(self):
        # Destroy the Tkinter root after each test
        self.root.destroy()

    def test_create_and_manage_shopping_lists(self):
        # Test creating a new shopping list
        self.app.list_name_entry.insert(0, "TestList")
        self.app.create_button.invoke()
        self.assertIn("TestList", self.app.shopping_list_manager.view_lists())

        # Test deleting the created shopping list
        self.app.shopping_list_manager.delete_list("TestList")
        self.assertNotIn("TestList", self.app.shopping_list_manager.view_lists())

    def test_add_and_categorize_items_in_list(self):
        # Create a list to add items to
        self.app.shopping_list_manager.create_list("TestList")

        # Test adding "Milk" to "Dairy" category
        self.app.list_name_entry.delete(0, tk.END)
        self.app.list_name_entry.insert(0, "TestList")
        self.app.item_entry.insert(0, "Milk")
        self.app.category_entry.insert(0, "Dairy")
        self.app.add_button.invoke()
        items = self.app.shopping_list_manager.lists["TestList"].get_items()
        self.assertIn("Milk", items.get("Dairy", []))

        # Test adding "Bread" to "Bakery" category
        self.app.item_entry.delete(0, tk.END)
        self.app.category_entry.delete(0, tk.END)
        self.app.item_entry.insert(0, "Bread")
        self.app.category_entry.insert(0, "Bakery")
        self.app.add_button.invoke()
        items = self.app.shopping_list_manager.lists["TestList"].get_items()
        self.assertIn("Bread", items.get("Bakery", []))

    def test_set_reminders_for_upcoming_shopping_trips(self):
        # This functionality is not implemented in the codebase
        self.fail("Set reminders functionality is not implemented.")

    def test_intuitive_and_simple_user_interface(self):
        # Test navigation through main menu options
        self.assertTrue(self.app.create_button.winfo_exists())
        self.assertTrue(self.app.view_button.winfo_exists())
        self.assertTrue(self.app.add_button.winfo_exists())

        # Test help button functionality (not implemented)
        self.fail("Help button functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
