import unittest
from data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data_analyzer = DataAnalyzer()

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\numerical_data.txt')
        self.assertEqual(self.data_analyzer.numerical_data, [1.5, 2.3, 3.7, 4.1, 5.0])
        self.assertEqual(self.data_analyzer.categorical_data, {})

    def test_calculate_mean(self):
        # Functionalities 2: Analyze numerical data to calculate the mean
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\numerical_data.txt')
        self.assertAlmostEqual(self.data_analyzer.calculate_mean(), 3.52)

    def test_calculate_median(self):
        # Functionalities 3: Analyze numerical data to calculate the median
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\numerical_data.txt')
        self.assertEqual(self.data_analyzer.calculate_median(), 3.7)

    def test_calculate_mode(self):
        # Functionalities 4: Analyze numerical data to calculate the mode
        self.data_analyzer.numerical_data = [1.5, 2.3, 2.3, 4.1, 5.0]  # Adding repeating values for mode
        self.assertEqual(self.data_analyzer.calculate_mode(), 2.3)

        self.data_analyzer.numerical_data = [1.5, 2.3, 4.1, 5.0]  # Unique values
        with self.assertRaises(ValueError):
            self.data_analyzer.calculate_mode()  # No mode should raise an error

    def test_calculate_range(self):
        # Functionalities 5: Analyze numerical data to calculate the range
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\numerical_data.txt')
        self.assertEqual(self.data_analyzer.calculate_range(), 3.5)  # 5.0 - 1.5

    def test_calculate_frequency(self):
        # Functionalities 6: Analyze categorical data to determine the frequency
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\categorical_data.txt')
        self.assertEqual(self.data_analyzer.calculate_frequency(), {'CategoryA': 10, 'CategoryB': 20, 'CategoryC': 30})

    def test_calculate_distribution(self):
        # Functionalities 7: Analyze categorical data to determine the distribution
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\categorical_data.txt')
        expected_distribution = {'CategoryA': 0.1, 'CategoryB': 0.2, 'CategoryC': 0.3}
        self.assertEqual(self.data_analyzer.calculate_distribution(), expected_distribution)

    def test_variable_selection(self):
        # Functionalities 8: Allow users to choose variables for analysis
        self.fail("not implemented")  # This functionality is not implemented in the codebase

    def test_display_summary(self):
        # Functionalities 9: Display the generated summary of the data
        self.data_analyzer.import_data('E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataSummarizer\\ce\\ce_0\\code\\numerical_data.txt')
        summary = self.data_analyzer.generate_summary()
        self.assertIn("Mean:", summary)
        self.assertIn("Median:", summary)
        self.assertIn("Mode:", summary)
        self.assertIn("Range:", summary)
        self.assertIn("Frequency:", summary)
        self.assertIn("Distribution:", summary)

if __name__ == '__main__':
    unittest.main()
