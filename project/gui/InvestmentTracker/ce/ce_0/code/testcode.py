import unittest
from investment_tracker import InvestmentTracker, Investment

class TestInvestmentTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = InvestmentTracker()
        self.tracker.load_data()

    def test_input_investment_details(self):
        # Functionalities 1: Input Investment Details
        investment_details = {
            'id': 2,
            'type': 'Bonds',
            'amount': 500.0,
            'date': '2023-10-02',
            'category': 'Fixed Income'
        }
        self.tracker.add_investment(investment_details)
        self.assertIn(Investment(**investment_details), self.tracker.investments)

    def test_categorize_investments(self):
        # Functionalities 2: Categorize Investments into Different Portfolios
        # Test Case 2.1
        self.tracker.categorize_investment(1, "Growth")
        self.assertEqual(self.tracker.investments[0].category, "Growth")

        # Test Case 2.2
        investment_details_2 = {
            'id': 3,
            'type': 'Real Estate',
            'amount': 2000.0,
            'date': '2023-10-03',
            'category': 'Balanced'
        }
        self.tracker.add_investment(investment_details_2)
        self.tracker.categorize_investment(3, "Income")
        self.assertEqual(self.tracker.investments[1].category, "Income")

    def test_provide_visualizations(self):
        # Functionalities 3: Provide Visualizations Showing Investment Performance Over Time
        # Test Case 3.1
        self.fail("not implemented")

        # Test Case 3.2
        self.fail("not implemented")

    def test_generate_reports(self):
        # Functionalities 4: Generate Reports on Investment Performance
        # Test Case 4.1
        self.fail("not implemented")

        # Test Case 4.2
        self.fail("not implemented")

    def test_set_investment_goals(self):
        # Functionalities 5: Set Investment Goals
        self.tracker.set_goal("Save $10,000 in 1 year")
        self.assertEqual(self.tracker.goals[0].description, "Save $10,000 in 1 year")

if __name__ == '__main__':
    unittest.main()
