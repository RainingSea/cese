import unittest
from investment_tracker import InvestmentTracker

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        self.tracker.add_investment("Investment C", "Stocks", 1500.0, "2023-03-01")
        self.assertEqual(len(self.tracker.investments), 3)
        self.assertEqual(self.tracker.investments[-1].name, "Investment C")
        self.assertEqual(self.tracker.investments[-1].type, "Stocks")
        self.assertEqual(self.tracker.investments[-1].amount, 1500.0)
        self.assertEqual(self.tracker.investments[-1].date, "2023-03-01")

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        self.tracker.categorize_investment("Investment A", "Growth")
        self.assertEqual(self.tracker.investments[0].type, "Growth")

        self.tracker.categorize_investment("Investment B", "Income")
        self.assertEqual(self.tracker.investments[1].type, "Income")

    def test_visualize_performance(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        # This functionality involves GUI and cannot be directly tested in a unit test without a display.
        # We will assume this functionality works as expected since it uses matplotlib to display a chart.
        self.fail("Visualization test not implemented due to GUI constraints")

    def test_generate_reports(self):
        # Functionalities 4: Generate Reports on Investment Performance
        report = self.tracker.generate_report()
        self.assertIn("Investment A: 1000.0 on 2023-01-01", report)
        self.assertIn("Investment B: 500.0 on 2023-02-01", report)

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        self.tracker.set_goal("Save $10,000 in 1 year")
        self.assertIn("Save $10,000 in 1 year", self.tracker.goals)
        self.assertFalse(self.tracker.goals["Save $10,000 in 1 year"])

if __name__ == '__main__':
    unittest.main()
