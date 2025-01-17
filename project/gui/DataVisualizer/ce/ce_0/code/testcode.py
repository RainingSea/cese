import unittest
import os
from data_visualizer import DataVisualizer
import matplotlib.pyplot as plt

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.data_visualizer = DataVisualizer()

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        try:
            self.data_visualizer.import_data('sample_data.csv')
            self.assertIsNotNone(self.data_visualizer.data)
        except Exception as e:
            self.fail(f"Importing data failed with exception: {e}")

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.data_visualizer.import_data('sample_data.csv')

        # Test creating a bar chart
        self.data_visualizer.visualization_type = 'bar'
        try:
            self.data_visualizer.create_visualization()
            plt.close()  # Close the plot to avoid displaying it during tests
        except Exception as e:
            self.fail(f"Creating bar chart failed with exception: {e}")

        # Test creating a scatter plot
        self.data_visualizer.visualization_type = 'scatter'
        try:
            self.data_visualizer.create_visualization()
            plt.close()  # Close the plot to avoid displaying it during tests
        except Exception as e:
            self.fail(f"Creating scatter plot failed with exception: {e}")

    def test_choose_appropriate_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        # This functionality is not implemented in the codebase
        self.fail("Recommended visualization feature not implemented")

    def test_customize_visualization(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.data_visualizer.import_data('sample_data.csv')
        self.data_visualizer.visualization_type = 'bar'
        self.data_visualizer.create_visualization()

        # Test changing color scheme (not implemented)
        self.fail("Change color scheme feature not implemented")

        # Test adjusting axis labels and chart title (not implemented)
        self.fail("Adjust axis labels and chart title feature not implemented")

        # Test enabling grid lines on scatter plot (not implemented)
        self.fail("Enable grid lines feature not implemented")

        # Test applying gradient fill to pie chart (not implemented)
        self.fail("Apply gradient fill feature not implemented")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.data_visualizer.import_data('sample_data.csv')
        self.data_visualizer.visualization_type = 'bar'
        self.data_visualizer.create_visualization()
        file_name = 'test_export.png'
        try:
            self.data_visualizer.export_visualization(file_name)
            self.assertTrue(os.path.exists(file_name))
        except Exception as e:
            self.fail(f"Exporting visualization failed with exception: {e}")
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
