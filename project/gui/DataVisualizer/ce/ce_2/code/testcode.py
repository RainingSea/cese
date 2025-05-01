import unittest
import os
from data_visualizer import DataVisualizer

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = DataVisualizer()
        self.test_csv_path = "E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataVisualizer\\ce\\ce_2\\code\\data.csv"
        self.invalid_csv_path = "invalid_path.csv"
        self.export_path = "E:\\Project\\ATE\\ATEdev\\ATEDev\\project\\gui\\DataVisualizer\\ce\\ce_2\\code\\visualization.png"

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        try:
            self.visualizer.import_data(self.test_csv_path)
            self.assertEqual(self.visualizer.data.get_data(), [10, 20, 30, 40, 50])
        except Exception as e:
            self.fail(f"Import data failed with exception: {e}")

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.visualizer.import_data(self.test_csv_path)

        # Test Bar Chart
        try:
            self.visualizer.create_visualization("Bar Chart")
        except Exception as e:
            self.fail(f"Bar Chart creation failed with exception: {e}")

        # Test Scatter Plot
        try:
            self.visualizer.create_visualization("Scatter Plot")
        except Exception as e:
            self.fail(f"Scatter Plot creation failed with exception: {e}")

    def test_choose_visualization_type(self):
        # Functionalities 3: Choose the appropriate type of visualization
        # This functionality is not implemented, so we will fail the test
        self.fail("Recommended visualization feature is not implemented.")

    def test_customize_visualization(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.visualizer.import_data(self.test_csv_path)

        # Test changing color scheme
        try:
            colors = ["#FF0000", "#00FF00", "#0000FF"]
            labels = ["Label1", "Label2", "Label3"]
            title = "Sample Visualization Title"
            self.visualizer.customize_visualization(colors, labels, title)
        except Exception as e:
            self.fail(f"Customization failed with exception: {e}")

        # Test enabling grid lines on a scatter plot
        # This functionality is not implemented, so we will fail the test
        self.fail("Enabling grid lines on scatter plot is not implemented.")

        # Test applying gradient fill to a pie chart
        # This functionality is not implemented, so we will fail the test
        self.fail("Applying gradient fill to pie chart is not implemented.")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.visualizer.import_data(self.test_csv_path)
        self.visualizer.create_visualization("Bar Chart")
        try:
            self.visualizer.export_visualization(self.export_path)
            self.assertTrue(os.path.exists(self.export_path))
        except Exception as e:
            self.fail(f"Export visualization failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
