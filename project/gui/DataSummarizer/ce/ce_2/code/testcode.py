import unittest
import os
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DataAnalyzer()
        self.sample_data_path = 'sample_data.csv'
        self.analyzer.import_data(self.sample_data_path)

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.analyzer.import_data(self.sample_data_path)
        self.assertIsNotNone(self.analyzer.data)
        self.assertIn('Column1', self.analyzer.data.columns)
        self.assertIn('Column2', self.analyzer.data.columns)

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        mean = self.analyzer.calculate_mean('Column1')
        self.assertEqual(mean, 5.5)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        median = self.analyzer.calculate_median('Column1')
        self.assertEqual(median, 5.5)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        mode = self.analyzer.calculate_mode('Column1')
        self.assertEqual(mode, 1)

        # Test with unique values
        self.analyzer.data['UniqueColumn'] = range(1, 11)
        mode_unique = self.analyzer.calculate_mode('UniqueColumn')
        self.assertEqual(mode_unique, 1)  # Since all are unique, the first value is returned

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        data_range = self.analyzer.calculate_range('Column1')
        self.assertEqual(data_range, (1, 10))

    def test_categorical_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        frequency = self.analyzer.categorical_frequency('Column2')
        expected_frequency = {'Apple': 4, 'Banana': 3, 'Orange': 3}
        self.assertEqual(frequency, expected_frequency)

    def test_categorical_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        distribution = self.analyzer.categorical_distribution('Column2')
        expected_distribution = {'Apple': 0.4, 'Banana': 0.3, 'Orange': 0.3}
        self.assertEqual(distribution, expected_distribution)

    def test_generate_summary(self):
        # Functionalities 9: Display the generated summary of the data
        selected_vars = ['Column1', 'Column2']
        summary = self.analyzer.generate_summary(selected_vars)
        self.assertIn("Summary for Column1:", summary)
        self.assertIn("Mean: 5.5", summary)
        self.assertIn("Median: 5.5", summary)
        self.assertIn("Mode: 1", summary)
        self.assertIn("Range: (1, 10)", summary)
        self.assertIn("Frequency: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}", summary)
        self.assertIn("Distribution: {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}", summary)

if __name__ == '__main__':
    unittest.main()
