import unittest
import pandas as pd
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DataAnalyzer()
        self.sample_data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace'],
            'Age': [30, 25, 35, 40, 22, 28, 30],
            'Salary': [70000, 50000, 120000, 80000, 45000, 60000, 75000]
        }
        self.analyzer.data = pd.DataFrame(self.sample_data)

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        try:
            self.analyzer.import_data('sample_data.csv')
            self.assertFalse(self.analyzer.data.empty)
        except Exception as e:
            self.fail(f"Import data failed with exception: {e}")

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        mean_age = self.analyzer.calculate_mean('Age')
        self.assertAlmostEqual(mean_age, 30, places=1)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        median_age = self.analyzer.calculate_median('Age')
        self.assertEqual(median_age, 30)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        mode_age = self.analyzer.calculate_mode('Age')
        self.assertEqual(mode_age, 30)

        # Test for unique values (no mode)
        self.analyzer.data['Unique'] = [1, 2, 3, 4, 5, 6, 7]
        mode_unique = self.analyzer.calculate_mode('Unique')
        self.assertEqual(mode_unique, 1)  # Since mode() returns the first value in case of no mode

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        age_range = self.analyzer.calculate_range('Age')
        self.assertEqual(age_range, (22, 40))

    def test_calculate_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        frequency_name = self.analyzer.calculate_frequency('Name')
        expected_frequency = {'Alice': 1, 'Bob': 1, 'Charlie': 1, 'David': 1, 'Eve': 1, 'Frank': 1, 'Grace': 1}
        self.assertEqual(frequency_name, expected_frequency)

    def test_calculate_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        distribution_name = self.analyzer.calculate_distribution('Name')
        expected_distribution = {'Alice': 1/7, 'Bob': 1/7, 'Charlie': 1/7, 'David': 1/7, 'Eve': 1/7, 'Frank': 1/7, 'Grace': 1/7}
        for name, proportion in expected_distribution.items():
            self.assertAlmostEqual(distribution_name[name], proportion, places=2)

    def test_generate_summary(self):
        # Functionalities 9: Display the generated summary of the data
        summary = self.analyzer.generate_summary(['Age', 'Salary'])
        self.assertIn('Age', summary)
        self.assertIn('Salary', summary)
        self.assertIn('mean', summary['Age'])
        self.assertIn('median', summary['Age'])
        self.assertIn('mode', summary['Age'])
        self.assertIn('range', summary['Age'])
        self.assertIn('frequency', summary['Age'])
        self.assertIn('distribution', summary['Age'])

if __name__ == '__main__':
    unittest.main()
