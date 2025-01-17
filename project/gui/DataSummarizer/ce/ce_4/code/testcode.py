import unittest
import pandas as pd
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data_analyzer = DataAnalyzer()
        self.sample_data = pd.DataFrame({
            'age': [25, 30, 22, 35, 28, 40],
            'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
            'income': [50000, 60000, 45000, 70000, 52000, 80000]
        })

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        data = self.data_analyzer.import_data('sample_data.csv')
        self.assertEqual(len(data), 6)
        self.assertIn('age', data.columns)
        self.assertIn('gender', data.columns)
        self.assertIn('income', data.columns)

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, ['age'])
        self.assertAlmostEqual(statistics['age']['mean'], 30)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, ['age'])
        self.assertEqual(statistics['age']['median'], 29)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, ['age'])
        self.assertEqual(statistics['age']['mode'], [25, 30, 22, 35, 28, 40])  # No mode

        # Adding a repeating value to test mode
        sample_data_with_mode = self.sample_data.copy()
        sample_data_with_mode.loc[0, 'age'] = 30
        statistics = self.data_analyzer.calculate_statistics(sample_data_with_mode, ['age'])
        self.assertEqual(statistics['age']['mode'], [30])

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        self.fail("not implemented")  # Range functionality not implemented in codebase

    def test_analyze_categorical_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, ['gender'])
        self.assertEqual(statistics['gender'], {'Male': 3, 'Female': 3})

    def test_analyze_categorical_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        self.fail("not implemented")  # Distribution functionality not implemented in codebase

    def test_select_variables_for_analysis(self):
        # Functionalities 8: Allow users to choose variables for analysis
        selected_columns = ['age', 'gender']
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, selected_columns)
        self.assertIn('age', statistics)
        self.assertIn('gender', statistics)

    def test_display_summary(self):
        # Functionalities 9: Display the generated summary of the data
        statistics = self.data_analyzer.calculate_statistics(self.sample_data, ['age', 'gender'])
        self.assertIn('age', statistics)
        self.assertIn('gender', statistics)
        self.assertIn('mean', statistics['age'])
        self.assertIn('median', statistics['age'])
        self.assertIn('mode', statistics['age'])
        self.assertIn('Male', statistics['gender'])
        self.assertIn('Female', statistics['gender'])

if __name__ == '__main__':
    unittest.main()
