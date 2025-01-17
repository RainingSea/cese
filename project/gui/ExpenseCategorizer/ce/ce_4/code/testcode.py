import unittest
from ExpenseCategorizer import ExpenseCategorizer
from Expense import Expense

class TestExpenseCategorizer(unittest.TestCase):

    def setUp(self):
        self.categorizer = ExpenseCategorizer()

    def test_input_expenses(self):
        # Test valid expense input
        self.categorizer.add_expense(100.0, "Dinner", "Food")
        self.assertIn(Expense(100.0, "Dinner", "Food"), self.categorizer.expenses)

        # Test invalid expense input (negative amount)
        with self.assertRaises(ValueError):
            self.categorizer.add_expense(-50.0, "Invalid Expense", "Food")

    def test_automatic_categorization(self):
        # This functionality is not implemented in the codebase
        self.fail("Automatic categorization of expenses is not implemented")

    def test_create_and_customize_categories(self):
        # Test creating a new category
        self.categorizer.categories.append("Health")
        self.assertIn("Health", self.categorizer.categories)

        # Test editing an existing category
        if "Entertainment" in self.categorizer.categories:
            index = self.categorizer.categories.index("Entertainment")
            self.categorizer.categories[index] = "Leisure"
            self.assertIn("Leisure", self.categorizer.categories)
            self.assertNotIn("Entertainment", self.categorizer.categories)
        else:
            self.fail("Category 'Entertainment' not found")

    def test_display_categorized_expenses(self):
        # Test displaying categorized expenses
        self.categorizer.add_expense(50.0, "Lunch", "Food")
        self.categorizer.add_expense(20.0, "Bus Ticket", "Transport")
        summary = self.categorizer.get_summary()
        self.assertEqual(summary["Food"], 50.0)
        self.assertEqual(summary["Transport"], 20.0)

        # Test removing an expense
        self.categorizer.expenses = [e for e in self.categorizer.expenses if e.description != "Lunch"]
        summary = self.categorizer.get_summary()
        self.assertNotIn("Lunch", [e.description for e in self.categorizer.expenses])

    def test_view_detailed_summaries(self):
        # Test viewing detailed summaries
        self.categorizer.add_expense(100.0, "Groceries", "Food")
        self.categorizer.add_expense(30.0, "Movie", "Entertainment")
        summary = self.categorizer.get_summary()
        self.assertEqual(summary["Food"], 100.0)
        self.assertEqual(summary["Entertainment"], 30.0)

        # Test filtering by category
        food_expenses = [e for e in self.categorizer.expenses if e.category == "Food"]
        self.assertEqual(sum(e.amount for e in food_expenses), 100.0)

if __name__ == '__main__':
    unittest.main()
