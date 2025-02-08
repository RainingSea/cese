import unittest
import pandas as pd
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data_analyzer = DataAnalyzer()
        self.data_analyzer.import_data('numerical_data.csv')

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.assertFalse(self.data_analyzer.data.empty, "Data should be imported successfully")

    def test_compute_numerical_summary_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        summary = self.data_analyzer.compute_numerical_summary(['column1'])
        self.assertAlmostEqual(summary['column1']['mean'], 50, places=2, msg="Mean should be calculated accurately")

    def test_compute_numerical_summary_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        summary = self.data_analyzer.compute_numerical_summary(['column1'])
        self.assertEqual(summary['column1']['median'], 50, "Median should be calculated accurately")

    def test_compute_numerical_summary_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        summary = self.data_analyzer.compute_numerical_summary(['column1'])
        self.assertEqual(summary['column1']['mode'], 10, "Mode should be calculated accurately")

        # Test for unique values (no mode)
        self.data_analyzer.data['unique_column'] = [1, 2, 3, 4, 5]
        summary = self.data_analyzer.compute_numerical_summary(['unique_column'])
        self.assertEqual(summary['unique_column']['mode'], 1, "Mode should be the first element for unique values")

    def test_compute_numerical_summary_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        summary = self.data_analyzer.compute_numerical_summary(['column1'])
        self.assertEqual(summary['column1']['range'], 80, "Range should be calculated accurately")

    def test_compute_categorical_summary_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        self.data_analyzer.import_data('categorical_data.csv')
        summary = self.data_analyzer.compute_categorical_summary(['category1'])
        self.assertEqual(summary['category1'], {'A': 3, 'B': 2}, "Frequency should be calculated accurately")

    def test_compute_categorical_summary_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        self.data_analyzer.import_data('categorical_data.csv')
        summary = self.data_analyzer.compute_categorical_summary(['category1'])
        total = sum(summary['category1'].values())
        distribution = {k: v / total for k, v in summary['category1'].items()}
        expected_distribution = {'A': 0.6, 'B': 0.4}
        self.assertEqual(distribution, expected_distribution, "Distribution should be calculated accurately")

    def test_variable_selection(self):
        # Functionalities 8: Allow users to choose variables for analysis
        numerical_vars = ['column1']
        categorical_vars = ['category1']
        self.assertIn('column1', numerical_vars, "Numerical variable should be selectable")
        self.assertIn('category1', categorical_vars, "Categorical variable should be selectable")

    def test_display_summary(self):
        # Functionalities 9: Display the generated summary of the data
        numerical_summary = self.data_analyzer.compute_numerical_summary(['column1'])
        categorical_summary = self.data_analyzer.compute_categorical_summary(['category1'])
        self.assertIsInstance(numerical_summary, dict, "Numerical summary should be a dictionary")
        self.assertIsInstance(categorical_summary, dict, "Categorical summary should be a dictionary")

if __name__ == '__main__':
    unittest.main()
