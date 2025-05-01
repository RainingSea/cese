import unittest
from data_handler import DataHandler

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.data_handler = DataHandler()
        # Importing numerical data for testing
        self.data_handler.import_data('numerical_data.txt')
        # Importing categorical data for testing
        self.data_handler.import_data('categorical_data.txt')

    def test_import_data_valid(self):
        # Functionalities 1: Import data sets into the application
        self.assertEqual(len(self.data_handler.numerical_data), 5)
        self.assertEqual(len(self.data_handler.categorical_data), 5)

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        mean = self.data_handler.calculate_mean(self.data_handler.numerical_data)
        self.assertAlmostEqual(mean, 3.52)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        median = self.data_handler.calculate_median(self.data_handler.numerical_data)
        self.assertEqual(median, 3.1)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        mode = self.data_handler.calculate_mode([1.5, 2.3, 2.3, 3.1, 4.7])
        self.assertEqual(mode, 2.3)

        # Testing with unique values
        mode_unique = self.data_handler.calculate_mode([1.5, 2.3, 3.1, 4.7])
        self.assertRaises(IndexError, lambda: self.data_handler.calculate_mode([1.5, 2.3, 3.1, 4.7]))

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        data_range = self.data_handler.calculate_range(self.data_handler.numerical_data)
        self.assertEqual(data_range, (1.5, 5.0))

    def test_calculate_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        frequency = self.data_handler.calculate_frequency(self.data_handler.categorical_data)
        self.assertEqual(frequency, {'apple': 2, 'banana': 2, 'orange': 1})

    def test_calculate_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        distribution = self.data_handler.calculate_distribution(self.data_handler.categorical_data)
        expected_distribution = {'apple': 0.4, 'banana': 0.4, 'orange': 0.2}
        for key in expected_distribution:
            self.assertAlmostEqual(distribution[key], expected_distribution[key])

    def test_get_variable_names(self):
        # Functionalities 8: Allow users to choose variables for analysis
        variable_names = self.data_handler.get_variable_names()
        self.assertEqual(variable_names, ['Variable1', 'Variable2', 'Variable3'])

    def test_generate_summary(self):
        # Functionalities 9: Display the generated summary of the data
        summary = self.data_handler.generate_summary()
        self.assertIn("Numerical Data Summary:", summary)
        self.assertIn("Categorical Data Summary:", summary)

if __name__ == '__main__':
    unittest.main()
