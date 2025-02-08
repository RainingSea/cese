import unittest
import os
import pandas as pd
from data_visualizer import DataVisualizer
import matplotlib.pyplot as plt

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = DataVisualizer()
        self.sample_data_path = "sample_data.csv"
        self.output_image_path = "test_output.png"

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        data = self.visualizer.import_data(self.sample_data_path)
        expected_data = {
            'Category': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'},
            'Value': {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}
        }
        self.assertEqual(data, expected_data)

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.visualizer.import_data(self.sample_data_path)

        # Test bar chart creation
        self.visualizer.visualization_type = "bar"
        self.visualizer.create_visualization()
        plt.close()

        # Test scatter plot creation
        self.visualizer.visualization_type = "scatter"
        self.visualizer.create_visualization()
        plt.close()

    def test_choose_appropriate_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        # This functionality is not implemented in the codebase
        self.fail("Recommended visualization feature not implemented")

    def test_customize_visualization(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.visualizer.import_data(self.sample_data_path)
        self.visualizer.visualization_type = "bar"

        # Test customization of axis labels and title
        options = {
            'title': 'Custom Title',
            'xlabel': 'Custom X-axis',
            'ylabel': 'Custom Y-axis'
        }
        self.visualizer.customize_visualization(options)
        self.visualizer.create_visualization()
        plt.close()

        # Test enabling grid lines on a scatter plot
        self.visualizer.visualization_type = "scatter"
        plt.grid(True)
        self.visualizer.create_visualization()
        plt.close()

        # Test gradient fill on a pie chart
        # This functionality is not implemented in the codebase
        self.fail("Gradient fill for pie chart not implemented")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.visualizer.import_data(self.sample_data_path)
        self.visualizer.visualization_type = "bar"
        self.visualizer.create_visualization()
        self.visualizer.export_visualization(self.output_image_path)
        plt.close()

        # Check if the file was created
        self.assertTrue(os.path.exists(self.output_image_path))

        # Clean up the created file
        if os.path.exists(self.output_image_path):
            os.remove(self.output_image_path)

if __name__ == '__main__':
    unittest.main()
