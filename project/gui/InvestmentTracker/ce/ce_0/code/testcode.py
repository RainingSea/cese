import unittest
from Investment import Investment
from Category import Category
from InvestmentTracker import InvestmentTracker
from data_management import load_investments, load_categories

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()
        self.tracker.categories = load_categories()
        self.tracker.investments = load_investments()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        investment = Investment("Test Investment", "Stocks", 1000.0, "2023-01-01")
        self.tracker.add_investment(investment)
        self.assertIn(investment, self.tracker.investments)

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        investment1 = Investment("Growth Investment", "Stocks", 2000.0, "2023-01-01")
        investment2 = Investment("Income Investment", "Bonds", 1500.0, "2023-02-01")
        
        self.tracker.add_investment(investment1)
        self.tracker.add_investment(investment2)
        
        self.tracker.categorize_investment(investment1, "Growth")
        self.tracker.categorize_investment(investment2, "Income")

        self.assertIn(investment1, [inv for cat in self.tracker.categories if cat.name == "Growth" for inv in cat.investments])
        self.assertIn(investment2, [inv for cat in self.tracker.categories if cat.name == "Income" for inv in cat.investments])

    def test_generate_report(self):
        # Functionalities 4: Generate Reports on Investment Performance
        report = self.tracker.generate_report()
        self.assertIn("Investment Report:", report)
        self.assertIn("Investment A: 1000.0 on 2023-01-01", report)
        self.assertIn("Investment B: 500.0 on 2023-02-01", report)
        self.assertIn("Investment C: 1500.0 on 2023-03-01", report)

    def test_set_investment_goal(self):
        # Functionalities 5: Set Investment Goals
        self.tracker.set_investment_goal("Save $10,000 in 1 year")
        self.assertEqual(self.tracker.investment_goal, "Save $10,000 in 1 year")

    def test_visualization_performance(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        # Since we cannot directly test the visualization, we will check if the function runs without error
        try:
            self.tracker.plot_performance()
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
