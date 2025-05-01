import unittest
import os
import pandas as pd
from main import DataVisualizer
from visualization import Visualization

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        # Create a DataVisualizer instance for testing
        self.visualizer = DataVisualizer(None)
        # Load sample data for testing
        self.sample_data_path = "E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataVisualizer\\ce\\ce_1\\code\\sample_data.csv"
        self.visualizer.data = pd.read_csv(self.sample_data_path)

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.visualizer.import_data()
        self.assertIsNotNone(self.visualizer.data, "Data should be imported successfully.")

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.visualizer.create_visualization("bar")  # Test bar chart creation
        self.visualizer.create_visualization("scatter")  # Test scatter plot creation

    def test_choose_appropriate_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        self.fail("not implemented")  # Placeholder for recommended visualization feature

    def test_customize_visualizations(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.fail("not implemented")  # Placeholder for customization features

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        # Create a temporary file path for testing export
        export_path = "E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataVisualizer\\ce\\ce_1\\code\\test_export.png"
        self.visualizer.visualizations.export(export_path)
        self.assertTrue(os.path.exists(export_path), "Exported image file should exist.")
        os.remove(export_path)  # Clean up the exported file after test

if __name__ == '__main__':
    unittest.main()
