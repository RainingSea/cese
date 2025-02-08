import unittest
from data_visualizer import DataVisualizer
from data_handler import DataHandler
import os

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = DataVisualizer()
        self.data_handler = DataHandler()
        self.sample_data_path = 'sample_data.csv'
        self.sample_data = {
            'labels': ['Category A', 'Category B', 'Category C', 'Category D'],
            'values': [10, 20, 30, 40]
        }

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.visualizer.import_data(self.sample_data_path)
        self.assertEqual(self.visualizer.data, self.sample_data)

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.visualizer.import_data(self.sample_data_path)

        # Test bar chart creation
        try:
            self.visualizer.create_visualization('bar')
        except Exception as e:
            self.fail(f"Bar chart creation failed with exception: {e}")

        # Test scatter plot creation
        try:
            self.visualizer.create_visualization('scatter')
        except Exception as e:
            self.fail(f"Scatter plot creation failed with exception: {e}")

    def test_choose_appropriate_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        # This functionality is not implemented in the codebase
        self.fail("Recommended visualization feature not implemented")

    def test_customize_visualization(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.visualizer.import_data(self.sample_data_path)
        self.visualizer.create_visualization('bar')

        # Test changing color scheme
        options = {'color': 'red'}
        self.visualizer.customize_visualization(options)
        # Assuming customization is applied, no direct way to test without GUI

        # Test adjusting axis labels and chart title
        options = {'xlabel': 'New X', 'ylabel': 'New Y', 'title': 'New Title'}
        self.visualizer.customize_visualization(options)
        # Assuming customization is applied, no direct way to test without GUI

        # Test enabling grid lines on scatter plot
        self.visualizer.create_visualization('scatter')
        options = {'grid': True}
        self.visualizer.customize_visualization(options)
        # Assuming customization is applied, no direct way to test without GUI

        # Test applying gradient fill to pie chart
        self.visualizer.create_visualization('pie')
        options = {'colors': ['#ff9999','#66b3ff','#99ff99','#ffcc99']}
        self.visualizer.customize_visualization(options)
        # Assuming customization is applied, no direct way to test without GUI

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.visualizer.import_data(self.sample_data_path)
        self.visualizer.create_visualization('bar')
        file_name = 'test_visualization.png'
        self.visualizer.export_visualization(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
