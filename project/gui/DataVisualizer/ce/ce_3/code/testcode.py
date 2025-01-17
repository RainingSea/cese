import unittest
import os
import pandas as pd
from data_visualizer import DataVisualizer

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = DataVisualizer()
        self.sample_data_path = 'sample_data.csv'
        self.sample_data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 20, 30, 40]
        })
        self.sample_data.to_csv(self.sample_data_path, index=False)

    def tearDown(self):
        if os.path.exists(self.sample_data_path):
            os.remove(self.sample_data_path)

    def test_import_data(self):
        # Functionalities 1: Import data sets into the application
        self.visualizer.import_data(self.sample_data_path)
        pd.testing.assert_frame_equal(self.visualizer.data, self.sample_data)

    def test_create_visualizations(self):
        # Functionalities 2: Create visualizations
        self.visualizer.import_data(self.sample_data_path)
        
        # Test bar chart creation
        try:
            self.visualizer.create_bar_chart()
        except Exception as e:
            self.fail(f"Bar chart creation failed with exception: {e}")

        # Test scatter plot creation
        try:
            self.visualizer.create_scatter_plot()
        except Exception as e:
            self.fail(f"Scatter plot creation failed with exception: {e}")

    def test_choose_appropriate_visualization(self):
        # Functionalities 3: Choose the appropriate type of visualization
        self.fail("not implemented")

    def test_customize_appearance(self):
        # Functionalities 4: Customize the appearance of the visualizations
        self.visualizer.import_data(self.sample_data_path)

        # Test changing color scheme
        try:
            self.visualizer.customize_appearance(colors=['#FF5733'], labels=self.sample_data['Category'].tolist())
        except Exception as e:
            self.fail(f"Color scheme customization failed with exception: {e}")

        # Test enabling grid lines on scatter plot
        try:
            plt.grid(True)
            self.visualizer.create_scatter_plot()
        except Exception as e:
            self.fail(f"Enabling grid lines failed with exception: {e}")

        # Test applying gradient fill to pie chart
        try:
            self.visualizer.create_pie_chart()
        except Exception as e:
            self.fail(f"Gradient fill application failed with exception: {e}")

    def test_export_visualization(self):
        # Functionalities 5: Export the visualization as an image
        self.visualizer.import_data(self.sample_data_path)
        self.visualizer.create_bar_chart()
        export_path = 'test_export.png'
        try:
            self.visualizer.export_visualization(export_path)
            self.assertTrue(os.path.exists(export_path))
        except Exception as e:
            self.fail(f"Export visualization failed with exception: {e}")
        finally:
            if os.path.exists(export_path):
                os.remove(export_path)

if __name__ == '__main__':
    unittest.main()
