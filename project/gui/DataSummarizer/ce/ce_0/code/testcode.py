import unittest
import pandas as pd
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data_analyzer = DataAnalyzer()
        # Load sample data for testing
        self.data_analyzer.load_data('sample_data.csv')

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.assertIsNotNone(self.data_analyzer.data)
        self.assertIn('Age', self.data_analyzer.data.columns)
        self.assertIn('Score', self.data_analyzer.data.columns)

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        mean_age = self.data_analyzer.calculate_mean('Age')
        self.assertAlmostEqual(mean_age, 27.8333, places=4)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        median_age = self.data_analyzer.calculate_median('Age')
        self.assertEqual(median_age, 28)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        mode_age = self.data_analyzer.calculate_mode('Age')
        self.assertEqual(mode_age, 22)

        # Test for unique values (no mode)
        mode_score = self.data_analyzer.calculate_mode('Score')
        self.assertIn(mode_score, [75, 82, 85, 88, 90, 95])  # Any value is valid as all are unique

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        age_range = self.data_analyzer.calculate_range('Age')
        self.assertEqual(age_range, (22, 35))

    def test_analyze_categorical(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        gender_frequency = self.data_analyzer.analyze_categorical('Gender')
        self.assertEqual(gender_frequency, {'Female': 3, 'Male': 3})

    def test_choose_variables(self):
        # Functionalities 8: Allow users to choose variables for analysis
        # This functionality is more related to UI, but we can check if variables can be selected
        columns = self.data_analyzer.data.columns.tolist()
        self.assertIn('Age', columns)
        self.assertIn('Gender', columns)

    def test_generate_summary(self):
        # Functionalities 9: Display the generated summary of the data
        summary = self.data_analyzer.generate_summary()
        self.assertIn('count', summary)
        self.assertIn('mean', summary)
        self.assertIn('std', summary)

if __name__ == '__main__':
    unittest.main()
