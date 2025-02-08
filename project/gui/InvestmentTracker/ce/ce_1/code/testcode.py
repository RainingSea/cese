import unittest
from main import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        initial_count = len(self.tracker.investments)
        self.tracker.add_investment("Stock", 1500.00, "Equity", "2023-04-01")
        self.assertEqual(len(self.tracker.investments), initial_count + 1)
        self.assertEqual(self.tracker.investments[-1].type, "Stock")
        self.assertEqual(self.tracker.investments[-1].amount, 1500.00)
        self.assertEqual(self.tracker.investments[-1].category, "Equity")
        self.assertEqual(self.tracker.investments[-1].date, "2023-04-01")

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        # Test Case 2.1
        self.tracker.add_investment("Stock", 1000.00, "Growth", "2023-01-15")
        self.assertEqual(self.tracker.investments[-1].category, "Growth")

        # Test Case 2.2
        self.tracker.add_investment("Bond", 500.00, "Income", "2023-02-20")
        self.tracker.add_investment("Real Estate", 2000.00, "Balanced", "2023-03-10")
        self.assertEqual(self.tracker.investments[-2].category, "Income")
        self.assertEqual(self.tracker.investments[-1].category, "Balanced")

    def test_visualize_performance(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        self.fail("not implemented")

    def test_generate_reports(self):
        # Functionalities 4: Generate Reports on Investment Performance
        self.fail("not implemented")

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        initial_count = len(self.tracker.goals)
        self.tracker.set_goal("Save for Car", 10000.00, "2024-12-31")
        self.assertEqual(len(self.tracker.goals), initial_count + 1)
        self.assertEqual(self.tracker.goals[-1].goal_name, "Save for Car")
        self.assertEqual(self.tracker.goals[-1].amount, 10000.00)
        self.assertEqual(self.tracker.goals[-1].deadline, "2024-12-31")

if __name__ == '__main__':
    unittest.main()
