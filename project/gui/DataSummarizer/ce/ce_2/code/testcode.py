import unittest
import json
from data_storage import DataAnalyzer, NumericalData, CategoricalData

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data_analyzer = DataAnalyzer()
        # Load numerical data for testing
        with open('numerical_data.json', 'r') as file:
            numerical_data = json.load(file)
            self.data_analyzer.numerical_data.load_data(numerical_data['numerical'])
        
        # Load categorical data for testing
        with open('categorical_data.json', 'r') as file:
            categorical_data = json.load(file)
            self.data_analyzer.categorical_data.load_data(categorical_data['categorical'])

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.assertIsNotNone(self.data_analyzer.numerical_data.data)
        self.assertIsNotNone(self.data_analyzer.categorical_data.data)

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        self.assertEqual(self.data_analyzer.calculate_mean(), 5.0)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        self.assertEqual(self.data_analyzer.calculate_median(), 5.0)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        self.data_analyzer.numerical_data.load_data([1, 2, 2, 3, 4])
        self.assertEqual(self.data_analyzer.calculate_mode(), [2])
        
        # Test with unique values
        self.data_analyzer.numerical_data.load_data([1, 2, 3, 4])
        self.assertEqual(self.data_analyzer.calculate_mode(), [1, 2, 3, 4])  # No mode

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        self.assertEqual(self.data_analyzer.calculate_range(), (1, 9))

    def test_calculate_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        frequency = self.data_analyzer.calculate_frequency()
        self.assertEqual(frequency, {'apple': 2, 'banana': 3, 'orange': 1})

    def test_calculate_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        distribution = self.data_analyzer.calculate_distribution()
        self.assertEqual(distribution, {'apple': 0.3333333333333333, 'banana': 0.5, 'orange': 0.16666666666666666})

    def test_generate_summary(self):
        # Functionalities 9: Display the generated summary of the data
        summary = self.data_analyzer.generate_summary()
        self.assertIn("Numerical Data Summary:", summary)
        self.assertIn("Mean: 5.0", summary)
        self.assertIn("Median: 5.0", summary)
        self.assertIn("Mode: [1, 2, 3, 4]", summary)  # Adjust based on the last mode test
        self.assertIn("Range: (1, 9)", summary)
        self.assertIn("Categorical Data Summary:", summary)
        self.assertIn("Frequency: {'apple': 2, 'banana': 3, 'orange': 1}", summary)

if __name__ == '__main__':
    unittest.main()
