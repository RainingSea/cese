import unittest
import os
from data_handler import DataHandler
from visualization import Visualization

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.data_handler = DataHandler()
        self.visualizer = Visualization()
        self.valid_csv_path = 'datasets/sample_data.csv'  # Path to the sample data
        self.export_image_path = 'exports/test_visualization.png'  # Path for exporting images

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        data = self.data_handler.import_data(self.valid_csv_path)
        self.assertGreater(len(data), 0, "Data import failed or returned empty data.")
        self.visualizer.data = data
        self.assertEqual(len(self.visualizer.data), 5, "Imported data does not match expected length.")

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        data = self.data_handler.import_data(self.valid_csv_path)
        self.visualizer.data = data
        
        # Test bar chart creation
        self.visualizer.create_bar_chart()  # This will show a plot, but we can't assert visual output

        # Test scatter plot creation
        self.visualizer.create_scatter_plot()  # This will show a plot, but we can't assert visual output

    def test_recommended_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        self.fail("Recommended visualization feature not implemented.")

    def test_customize_appearance(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.visualizer.customize_appearance({'color_scheme': 'blue'})
        self.fail("Customization feature not implemented.")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        data = self.data_handler.import_data(self.valid_csv_path)
        self.visualizer.data = data
        self.visualizer.create_bar_chart()  # Create a chart before exporting
        self.visualizer.export_image(self.export_image_path)
        self.assertTrue(os.path.exists(self.export_image_path), "Exported image file does not exist.")
        os.remove(self.export_image_path)  # Clean up after test

if __name__ == '__main__':
    unittest.main()
