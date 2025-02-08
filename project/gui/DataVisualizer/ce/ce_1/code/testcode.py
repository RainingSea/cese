import unittest
from data_visualizer import DataVisualizer
import os

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.data_visualizer = DataVisualizer()
        self.sample_data_path = 'sample_data.csv'
        self.export_path = 'test_export.png'

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        data = self.data_visualizer.import_data(self.sample_data_path)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)  # Assuming the sample data has 2 rows

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        data = self.data_visualizer.import_data(self.sample_data_path)
        options = {'color': 'green', 'xlabel': 'Categories', 'ylabel': 'Values', 'title': 'Sample Bar Chart'}
        
        # Test bar chart creation
        try:
            self.data_visualizer.create_visualization('bar', data, options)
        except Exception as e:
            self.fail(f"Bar chart creation failed with exception: {e}")

        # Test scatter plot creation
        try:
            self.data_visualizer.create_visualization('scatter', data, options)
        except Exception as e:
            self.fail(f"Scatter plot creation failed with exception: {e}")

    def test_choose_visualization_type(self):
        # Functionalities 3: Choose the appropriate type of visualization
        self.fail("not implemented")  # This feature is not implemented in the codebase

    def test_customize_visualization(self):
        # Functionalities 4: Customize the appearance of the visualizations
        data = self.data_visualizer.import_data(self.sample_data_path)
        options = {'color': 'blue', 'xlabel': 'New X', 'ylabel': 'New Y', 'title': 'New Title'}

        # Test color scheme change
        try:
            self.data_visualizer.create_visualization('bar', data, options)
        except Exception as e:
            self.fail(f"Customization failed with exception: {e}")

        # Test enabling grid lines on scatter plot
        options['grid'] = True
        try:
            self.data_visualizer.create_visualization('scatter', data, options)
        except Exception as e:
            self.fail(f"Grid line enabling failed with exception: {e}")

        # Test gradient fill on pie chart
        self.fail("Gradient fill customization not implemented")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.fail("Export functionality not implemented")

    def tearDown(self):
        # Clean up any files created during tests
        if os.path.exists(self.export_path):
            os.remove(self.export_path)

if __name__ == '__main__':
    unittest.main()
